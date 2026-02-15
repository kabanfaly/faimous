from app import db
from app.models import Product


def list_products(organisation_id):
    return Product.query.filter_by(organisation_id=organisation_id).order_by(Product.name).all()


def create_product(organisation_id, data):
    product = Product(
        organisation_id=organisation_id,
        name=data["name"],
        description=data.get("description"),
        type=data.get("type"),
        unit=data.get("unit"),
    )
    db.session.add(product)
    db.session.commit()
    return product


def get_product(organisation_id, product_id):
    return Product.query.filter_by(id=product_id, organisation_id=organisation_id).first()


def update_product(product, data):
    if "name" in data:
        product.name = data["name"]
    if "description" in data:
        product.description = data["description"]
    if "type" in data:
        product.type = data["type"]
    if "unit" in data:
        product.unit = data["unit"]
    db.session.commit()
    return product


def delete_product(product):
    db.session.delete(product)
    db.session.commit()
