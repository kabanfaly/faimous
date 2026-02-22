from decimal import Decimal
from app import db
from app.models import Purchase, SupplierPayment, Supplier, City


def get_organisation_id():
    from app.multi_tenant.context import get_current_organisation_id
    return get_current_organisation_id()


def create_purchase(organisation_id, data):
    purchase = Purchase(
        date=data["date"],
        supplier_id=data.get("supplier_id"),
        product_id=data.get("product_id"),
        unit_price=data.get("unit_price"),
        quantity=data.get("quantity", 0),
        total_price=data.get("total_price"),
        status=data.get("status", "unpaid"),
        currency=data.get("currency"),
        amount_base=data.get("amount_base"),
    )
    db.session.add(purchase)
    db.session.commit()
    return purchase


def add_supplier_payment(purchase_id, organisation_id, data):
    purchase = (
        Purchase.query.join(Supplier, Purchase.supplier_id == Supplier.id)
        .join(City, Supplier.city_id == City.id)
        .filter(Purchase.id == purchase_id, City.organisation_id == organisation_id)
        .first()
    )
    if not purchase:
        return None
    payment = SupplierPayment(
        purchase_id=purchase_id,
        date=data["date"],
        amount=data["amount"],
        payment_method=data.get("payment_method"),
        note=data.get("note"),
    )
    db.session.add(payment)
    total_paid = db.session.query(db.func.sum(SupplierPayment.amount)).filter(
        SupplierPayment.purchase_id == purchase_id
    ).scalar() or Decimal(0)
    total_paid += data["amount"]
    purchase_total = purchase.total_price or purchase.amount_base or Decimal(0)
    purchase.status = "paid" if total_paid >= purchase_total else "partial"
    db.session.commit()
    return payment


def get_unpaid_purchases(organisation_id):
    return (
        Purchase.query.join(Supplier, Purchase.supplier_id == Supplier.id)
        .join(City, Supplier.city_id == City.id)
        .filter(City.organisation_id == organisation_id)
        .filter(Purchase.status.in_(["unpaid", "partial"]))
        .order_by(Purchase.date.desc())
        .all()
    )


def get_purchase(organisation_id, purchase_id):
    return (
        Purchase.query.join(Supplier, Purchase.supplier_id == Supplier.id)
        .join(City, Supplier.city_id == City.id)
        .filter(Purchase.id == purchase_id, City.organisation_id == organisation_id)
        .first()
    )


def update_purchase(purchase, data):
    if "date" in data:
        purchase.date = data["date"]
    if "supplier_id" in data:
        purchase.supplier_id = data["supplier_id"]
    if "product_id" in data:
        purchase.product_id = data["product_id"]
    if "unit_price" in data:
        purchase.unit_price = data["unit_price"]
    if "quantity" in data:
        purchase.quantity = data["quantity"]
    if "total_price" in data:
        purchase.total_price = data["total_price"]
    if "status" in data:
        purchase.status = data["status"]
    db.session.commit()
    return purchase


def delete_purchase(purchase):
    db.session.delete(purchase)
    db.session.commit()
