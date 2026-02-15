from decimal import Decimal
from sqlalchemy import func
from app import db
from app.models import Product, StockMovement


def get_organisation_id():
    from app.multi_tenant.context import get_current_organisation_id
    return get_current_organisation_id()


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


def list_stock_movements(organisation_id, product_id=None):
    q = StockMovement.query.filter_by(organisation_id=organisation_id)
    if product_id:
        q = q.filter_by(product_id=product_id)
    return q.order_by(StockMovement.date.desc()).all()


def create_stock_movement(organisation_id, data):
    movement = StockMovement(
        organisation_id=organisation_id,
        date=data["date"],
        product_id=data["product_id"],
        description=data.get("description"),
        quantity=data["quantity"],
        price=data.get("price"),
        movement_type=data.get("movement_type"),
        purchase_id=data.get("purchase_id"),
    )
    db.session.add(movement)
    db.session.commit()
    return movement


def get_stock_movement(organisation_id, movement_id):
    return StockMovement.query.filter_by(id=movement_id, organisation_id=organisation_id).first()


def update_stock_movement(movement, data):
    if "date" in data:
        movement.date = data["date"]
    if "product_id" in data:
        movement.product_id = data["product_id"]
    if "description" in data:
        movement.description = data["description"]
    if "quantity" in data:
        movement.quantity = data["quantity"]
    if "price" in data:
        movement.price = data["price"]
    if "movement_type" in data:
        movement.movement_type = data["movement_type"]
    db.session.commit()
    return movement


def delete_stock_movement(movement):
    db.session.delete(movement)
    db.session.commit()


def get_stock_balance(organisation_id, product_id=None):
    q = db.session.query(
        StockMovement.product_id,
        func.sum(StockMovement.quantity).label("balance"),
    ).filter(
        StockMovement.organisation_id == organisation_id,
    )
    if product_id:
        q = q.filter(StockMovement.product_id == product_id)
    q = q.group_by(StockMovement.product_id)
    return q.all()


def get_low_stock_alerts(organisation_id, threshold=0):
    balances = get_stock_balance(organisation_id)
    alerts = []
    for product_id, balance in balances:
        if balance is None:
            continue
        b = float(balance)
        if b <= threshold:
            product = Product.query.get(product_id)
            if product:
                alerts.append({"product_id": product_id, "product_name": product.name, "balance": b})
    return alerts
