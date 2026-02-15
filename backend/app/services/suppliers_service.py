from app import db
from app.models import Supplier


def list_suppliers(organisation_id):
    return Supplier.query.filter_by(organisation_id=organisation_id).order_by(Supplier.name).all()


def create_supplier(organisation_id, data):
    supplier = Supplier(
        organisation_id=organisation_id,
        name=data["name"],
        phone=data.get("phone"),
        email=data.get("email"),
        city_id=data.get("city_id"),
    )
    db.session.add(supplier)
    db.session.commit()
    return supplier


def get_supplier(organisation_id, supplier_id):
    return Supplier.query.filter_by(id=supplier_id, organisation_id=organisation_id).first()


def update_supplier(supplier, data):
    if "name" in data:
        supplier.name = data["name"]
    if "phone" in data:
        supplier.phone = data["phone"]
    if "email" in data:
        supplier.email = data["email"]
    if "city_id" in data:
        supplier.city_id = data["city_id"]
    db.session.commit()
    return supplier


def delete_supplier(supplier):
    db.session.delete(supplier)
    db.session.commit()
