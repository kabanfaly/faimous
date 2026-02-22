from app import db
from app.models import Product


def list_products(organisation_id):
    return Product.query.order_by(Product.name).all()


def create_product(organisation_id, data):
    product = Product(
        product_type_id=data.get("product_type_id"),
        name=data["name"],
        description=data.get("description"),
        unit=data.get("unit"),
    )
    db.session.add(product)
    db.session.commit()
    return product


def get_product(organisation_id, product_id):
    product = Product.query.get(product_id)
    if not product:
        return None
    return product


def update_product(product, data):
    if "name" in data:
        product.name = data["name"]
    if "description" in data:
        product.description = data["description"]
    if "product_type_id" in data:
        product.product_type_id = data["product_type_id"]
    if "unit" in data:
        product.unit = data["unit"]
    db.session.commit()
    return product


def delete_product(product):
    db.session.delete(product)
    db.session.commit()
