from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy import func
from app import db
from app.models import (
    EggProduction,
    FlockRecord,
    Sale,
    PaymentReceived,
    Purchase,
    SupplierPayment,
    Expense,
    Contribution,
    StockMovement,
    Product,
)


def get_organisation_id():
    from app.multi_tenant.context import get_current_organisation_id
    return get_current_organisation_id()


def get_dashboard_summary(organisation_id):
    today = date.today()
    month_start = today.replace(day=1)
    week_start = today - timedelta(days=today.weekday())

    eggs_today = db.session.query(func.coalesce(func.sum(EggProduction.eggs_count), 0)).filter(
        EggProduction.organisation_id == organisation_id,
        EggProduction.date == today,
    ).scalar() or 0
    eggs_week = db.session.query(func.coalesce(func.sum(EggProduction.eggs_count), 0)).filter(
        EggProduction.organisation_id == organisation_id,
        EggProduction.date >= week_start,
        EggProduction.date <= today,
    ).scalar() or 0
    eggs_month = db.session.query(func.coalesce(func.sum(EggProduction.eggs_count), 0)).filter(
        EggProduction.organisation_id == organisation_id,
        EggProduction.date >= month_start,
        EggProduction.date <= today,
    ).scalar() or 0

    latest_flock = db.session.query(FlockRecord).filter(
        FlockRecord.organisation_id == organisation_id,
    ).order_by(FlockRecord.date.desc()).first()
    current_hens = (latest_flock.total_hens - latest_flock.dead) if latest_flock else 0

    total_sales = db.session.query(
        func.coalesce(func.sum(Sale.amount_base), func.sum(Sale.total_price), 0)
    ).filter(Sale.organisation_id == organisation_id).scalar() or Decimal(0)
    total_received = Decimal(0)
    for s in Sale.query.filter_by(organisation_id=organisation_id).all():
        total_received += db.session.query(func.coalesce(func.sum(PaymentReceived.amount), 0)).filter(
            PaymentReceived.sale_id == s.id
        ).scalar() or Decimal(0)
    outstanding_sales = float(total_sales - total_received)

    total_purchases = db.session.query(
        func.coalesce(func.sum(Purchase.amount_base), func.sum(Purchase.total_price), 0)
    ).filter(Purchase.organisation_id == organisation_id).scalar() or Decimal(0)
    total_supplier_paid = Decimal(0)
    for p in Purchase.query.filter_by(organisation_id=organisation_id).all():
        total_supplier_paid += db.session.query(func.coalesce(func.sum(SupplierPayment.amount), 0)).filter(
            SupplierPayment.purchase_id == p.id
        ).scalar() or Decimal(0)
    outstanding_purchases = float(total_purchases - total_supplier_paid)

    total_expenses = db.session.query(
        func.coalesce(func.sum(Expense.amount_base), func.sum(Expense.amount), 0)
    ).filter(Expense.organisation_id == organisation_id).scalar() or Decimal(0)
    total_contributions = db.session.query(
        func.coalesce(func.sum(Contribution.amount_base), func.sum(Contribution.amount), 0)
    ).filter(Contribution.organisation_id == organisation_id).scalar() or Decimal(0)
    result = float(total_received - total_supplier_paid - total_expenses + total_contributions)

    stock_value = db.session.query(
        func.coalesce(func.sum(StockMovement.quantity * func.coalesce(StockMovement.price, 0)), 0)
    ).filter(StockMovement.organisation_id == organisation_id).scalar() or Decimal(0)

    return {
        "production": {
            "eggs_today": eggs_today,
            "eggs_week": eggs_week,
            "eggs_month": eggs_month,
            "current_hens": current_hens,
        },
        "finance": {
            "revenue": float(total_sales),
            "received": float(total_received),
            "outstanding_sales": outstanding_sales,
            "outstanding_purchases": outstanding_purchases,
            "result": result,
        },
        "stock": {
            "value": float(stock_value),
        },
        "alerts": [],
    }


def get_dashboard_charts(organisation_id):
    today = date.today()
    from_date = today - timedelta(days=90)

    egg_dates = db.session.query(
        EggProduction.date,
        func.sum(EggProduction.eggs_count).label("total"),
    ).filter(
        EggProduction.organisation_id == organisation_id,
        EggProduction.date >= from_date,
        EggProduction.date <= today,
    ).group_by(EggProduction.date).order_by(EggProduction.date).all()

    egg_production = [{"date": str(d), "eggs": int(t or 0)} for d, t in egg_dates]

    return {
        "egg_production": egg_production,
    }
