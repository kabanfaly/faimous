from datetime import date, timedelta
from sqlalchemy import func
from app import db
from app.models import EggProduction, FlockRecord, DailyOperation, Farm


def get_organisation_id():
    from app.multi_tenant.context import get_current_organisation_id
    return get_current_organisation_id()


def create_egg_production(organisation_id, data):
    from app.models import EggProduction
    rec = EggProduction(
        farm_id=data.get("farm_id"),
        date=data["date"],
        eggs_count=data.get("eggs_count", 0),
        broken_count=data.get("broken_count", 0),
        trays=data.get("trays"),
        remaining=data.get("remaining"),
        note=data.get("note"),
    )
    db.session.add(rec)
    db.session.commit()
    return rec


def create_flock_record(organisation_id, data):
    from app.models import FlockRecord
    rec = FlockRecord(
        farm_id=data.get("farm_id"),
        date=data["date"],
        total_hens=data.get("total_hens", 0),
        dead=data.get("dead", 0),
        note=data.get("note"),
    )
    db.session.add(rec)
    db.session.commit()
    return rec


def list_daily_operations(organisation_id):
    return (
        DailyOperation.query.join(Farm, DailyOperation.farm_id == Farm.id)
        .order_by(DailyOperation.date.desc())
        .all()
    )


def get_daily_operation(organisation_id, operation_id):
    return (
        DailyOperation.query.join(Farm, DailyOperation.farm_id == Farm.id)
        .filter(DailyOperation.id == operation_id)
        .first()
    )


def create_daily_operation(organisation_id, data):
    from app.models import DailyOperation
    rec = DailyOperation(
        farm_id=data.get("farm_id"),
        date=data["date"],
        period=data.get("period"),
        collect1=data.get("collect1"),
        collect2=data.get("collect2"),
        collect3=data.get("collect3"),
        collect4=data.get("collect4"),
        broken=data.get("broken"),
        hens=data.get("hens"),
        dead=data.get("dead"),
    )
    db.session.add(rec)
    db.session.commit()
    return rec


def update_daily_operation(rec, data):
    if "farm_id" in data:
        rec.farm_id = data["farm_id"]
    if "date" in data:
        rec.date = data["date"]
    if "period" in data:
        rec.period = data["period"]
    if "collect1" in data:
        rec.collect1 = data["collect1"]
    if "collect2" in data:
        rec.collect2 = data["collect2"]
    if "collect3" in data:
        rec.collect3 = data["collect3"]
    if "collect4" in data:
        rec.collect4 = data["collect4"]
    if "broken" in data:
        rec.broken = data["broken"]
    if "hens" in data:
        rec.hens = data["hens"]
    if "dead" in data:
        rec.dead = data["dead"]
    db.session.commit()
    return rec


def delete_daily_operation(rec):
    db.session.delete(rec)
    db.session.commit()


def get_production_kpis(organisation_id):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    eggs_today = db.session.query(func.coalesce(func.sum(EggProduction.eggs_count), 0)).join(
        Farm, EggProduction.farm_id == Farm.id
    ).filter(
        EggProduction.date == today,
    ).scalar() or 0

    eggs_week = db.session.query(func.coalesce(func.sum(EggProduction.eggs_count), 0)).join(
        Farm, EggProduction.farm_id == Farm.id
    ).filter(
        EggProduction.date >= week_start,
        EggProduction.date <= today,
    ).scalar() or 0

    eggs_month = db.session.query(func.coalesce(func.sum(EggProduction.eggs_count), 0)).join(
        Farm, EggProduction.farm_id == Farm.id
    ).filter(
        EggProduction.date >= month_start,
        EggProduction.date <= today,
    ).scalar() or 0

    total_eggs = db.session.query(func.coalesce(func.sum(EggProduction.eggs_count), 0)).join(
        Farm, EggProduction.farm_id == Farm.id
    ).scalar() or 0
    total_broken = db.session.query(func.coalesce(func.sum(EggProduction.broken_count), 0)).join(
        Farm, EggProduction.farm_id == Farm.id
    ).scalar() or 0
    break_rate = (float(total_broken) / (total_eggs + total_broken) * 100) if (total_eggs + total_broken) else 0

    latest_flock = db.session.query(FlockRecord).join(
        Farm, FlockRecord.farm_id == Farm.id
    ).order_by(FlockRecord.date.desc()).first()
    current_hens = latest_flock.total_hens - latest_flock.dead if latest_flock else 0
    mortality = latest_flock.dead if latest_flock else 0

    return {
        "eggs_today": eggs_today,
        "eggs_week": eggs_week,
        "eggs_month": eggs_month,
        "break_rate": round(break_rate, 2),
        "current_hens": current_hens,
        "mortality": mortality,
    }
