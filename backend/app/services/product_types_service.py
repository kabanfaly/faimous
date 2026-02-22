from app import db
from app.models import ProductType


def list_product_types():
    return ProductType.query.order_by(ProductType.name).all()


def create_product_type(data):
    pt = ProductType(name=data["name"], farm_id=data["farm_id"])
    db.session.add(pt)
    db.session.commit()
    return pt


def get_product_type(product_type_id):
    return ProductType.query.get(product_type_id)


def update_product_type(product_type, data):
    if "name" in data:
        product_type.name = data["name"]
    if "farm_id" in data:
        product_type.farm_id = data["farm_id"]
    db.session.commit()
    return product_type


def delete_product_type(product_type):
    if product_type.products:
        raise ValueError("Cannot delete product type: it is used by products")
    db.session.delete(product_type)
    db.session.commit()
