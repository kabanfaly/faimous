from decimal import Decimal
from app import db
from app.models import Sale, PaymentReceived


def get_organisation_id():
    from app.multi_tenant.context import get_current_organisation_id
    return get_current_organisation_id()


def create_sale(organisation_id, data):
    sale = Sale(
        organisation_id=organisation_id,
        date=data["date"],
        type=data.get("type"),
        quantity=data.get("quantity", 0),
        unit_price=data.get("unit_price"),
        total_price=data.get("total_price"),
        theoretical_price=data.get("theoretical_price"),
        price_diff=data.get("price_diff"),
        wholesaler_id=data.get("wholesaler_id"),
        payment_status=data.get("payment_status", "unpaid"),
        currency=data.get("currency"),
        amount_base=data.get("amount_base"),
    )
    db.session.add(sale)
    db.session.commit()
    return sale


def add_payment_received(sale_id, organisation_id, data):
    sale = Sale.query.filter_by(id=sale_id, organisation_id=organisation_id).first()
    if not sale:
        return None
    payment = PaymentReceived(
        sale_id=sale_id,
        date=data["date"],
        amount=data["amount"],
        payment_method=data.get("payment_method"),
        note=data.get("note"),
    )
    db.session.add(payment)
    total_paid = db.session.query(db.func.sum(PaymentReceived.amount)).filter(
        PaymentReceived.sale_id == sale_id
    ).scalar() or Decimal(0)
    total_paid += data["amount"]
    sale_total = sale.total_price or sale.amount_base or Decimal(0)
    sale.payment_status = "paid" if total_paid >= sale_total else "partial"
    db.session.commit()
    return payment


def get_unpaid_sales(organisation_id):
    return Sale.query.filter_by(
        organisation_id=organisation_id,
    ).filter(
        Sale.payment_status.in_(["unpaid", "partial"])
    ).order_by(Sale.date.desc()).all()


def get_sale(organisation_id, sale_id):
    return Sale.query.filter_by(id=sale_id, organisation_id=organisation_id).first()


def update_sale(sale, data):
    if "date" in data:
        sale.date = data["date"]
    if "type" in data:
        sale.type = data["type"]
    if "quantity" in data:
        sale.quantity = data["quantity"]
    if "unit_price" in data:
        sale.unit_price = data["unit_price"]
    if "total_price" in data:
        sale.total_price = data["total_price"]
    if "payment_status" in data:
        sale.payment_status = data["payment_status"]
    db.session.commit()
    return sale


def delete_sale(sale):
    db.session.delete(sale)
    db.session.commit()
