from decimal import Decimal
from datetime import date, timedelta
from sqlalchemy import func
from app import db
from app.models import Sale, PaymentReceived, Purchase, SupplierPayment, Supplier, City, Expense, Contribution, Shareholder, Farm


def get_organisation_id():
    from app.multi_tenant.context import get_current_organisation_id
    return get_current_organisation_id()


def get_finance_result(organisation_id):
    revenue = (
        db.session.query(
            func.coalesce(func.sum(Sale.amount_base), func.sum(Sale.total_price), 0)
        )
        .join(Farm, Sale.farm_id == Farm.id)
        .scalar()
        or Decimal(0)
    )

    total_received = Decimal(0)
    for s in Sale.query.join(Farm, Sale.farm_id == Farm.id).all():
        total_received += db.session.query(func.coalesce(func.sum(PaymentReceived.amount), 0)).filter(
            PaymentReceived.sale_id == s.id
        ).scalar() or Decimal(0)

    purchases_total = (
        db.session.query(
            func.coalesce(func.sum(Purchase.amount_base), func.sum(Purchase.total_price), 0)
        )
        .join(Supplier, Purchase.supplier_id == Supplier.id)
        .join(City, Supplier.city_id == City.id)
        .filter(City.organisation_id == organisation_id)
        .scalar()
        or Decimal(0)
    )

    total_supplier_paid = Decimal(0)
    for p in (
        Purchase.query.join(Supplier, Purchase.supplier_id == Supplier.id)
        .join(City, Supplier.city_id == City.id)
        .filter(City.organisation_id == organisation_id)
        .all()
    ):
        total_supplier_paid += db.session.query(func.coalesce(func.sum(SupplierPayment.amount), 0)).filter(
            SupplierPayment.purchase_id == p.id
        ).scalar() or Decimal(0)

    total_expenses = db.session.query(
        func.coalesce(func.sum(Expense.amount_base), func.sum(Expense.amount), 0)
    ).join(Farm, Expense.farm_id == Farm.id).scalar() or Decimal(0)

    total_contributions = (
        db.session.query(
            func.coalesce(func.sum(Contribution.amount_base), func.sum(Contribution.amount), 0)
        )
        .join(Shareholder, Contribution.shareholder_id == Shareholder.id)
        .filter(Shareholder.organisation_id == organisation_id)
        .scalar()
        or Decimal(0)
    )

    outstanding_sales = revenue - total_received
    outstanding_purchases = purchases_total - total_supplier_paid
    result = total_received - total_supplier_paid - total_expenses + total_contributions

    return {
        "revenue": float(revenue),
        "received": float(total_received),
        "outstanding_sales": float(outstanding_sales),
        "purchases": float(purchases_total),
        "supplier_paid": float(total_supplier_paid),
        "outstanding_purchases": float(outstanding_purchases),
        "expenses": float(total_expenses),
        "contributions": float(total_contributions),
        "result": float(result),
    }


def get_cashflow(organisation_id, from_date=None, to_date=None):
    if not to_date:
        to_date = date.today()
    if not from_date:
        from_date = to_date - timedelta(days=365)

    inflows = (
        db.session.query(
            func.date(PaymentReceived.date).label("d"),
            func.sum(PaymentReceived.amount).label("amount"),
        )
        .join(Sale)
        .join(Farm, Sale.farm_id == Farm.id)
        .filter(
            PaymentReceived.date >= from_date,
            PaymentReceived.date <= to_date,
        )
        .group_by(func.date(PaymentReceived.date))
        .all()
    )

    outflows_purchases = (
        db.session.query(
            func.date(SupplierPayment.date).label("d"),
            -func.sum(SupplierPayment.amount).label("amount"),
        )
        .join(Purchase)
        .join(Supplier, Purchase.supplier_id == Supplier.id)
        .join(City, Supplier.city_id == City.id)
        .filter(
            City.organisation_id == organisation_id,
            SupplierPayment.date >= from_date,
            SupplierPayment.date <= to_date,
        )
        .group_by(func.date(SupplierPayment.date))
        .all()
    )

    outflows_expenses = db.session.query(
        func.date(Expense.date).label("d"),
        -func.sum(Expense.amount).label("amount"),
    ).join(Farm, Expense.farm_id == Farm.id).filter(
        Expense.date >= from_date,
        Expense.date <= to_date,
    ).group_by(Expense.date).all()

    inflows_dict = {str(d): float(a) for d, a in inflows}
    outflows_dict = {}
    for d, a in outflows_purchases:
        k = str(d)
        outflows_dict[k] = outflows_dict.get(k, 0) + float(a or 0)
    for d, a in outflows_expenses:
        k = str(d)
        outflows_dict[k] = outflows_dict.get(k, 0) + float(a or 0)

    all_dates = sorted(set(inflows_dict.keys()) | set(outflows_dict.keys()))
    series = []
    for d in all_dates:
        inc = inflows_dict.get(d, 0)
        out = outflows_dict.get(d, 0)
        series.append({"date": d, "inflow": inc, "outflow": abs(out), "net": inc + out})

    return {"series": series}
