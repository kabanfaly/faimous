from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.stock_service import (
    list_products,
    create_product,
    get_product,
    update_product as update_product_svc,
    delete_product as delete_product_svc,
    list_stock_movements,
    create_stock_movement,
    get_stock_movement,
    update_stock_movement,
    delete_stock_movement,
    get_low_stock_alerts,
)
from app.schemas.stock import ProductSchema, StockMovementSchema

stock_bp = Blueprint("stock", __name__)
product_schema = ProductSchema()
movement_schema = StockMovementSchema()


@stock_bp.route("/products", methods=["GET"])
@jwt_required()
def get_products():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    products = list_products(org_id)
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "product_type_id": p.product_type_id,
            "product_type": {"id": p.product_type.id, "name": p.product_type.name} if p.product_type else None,
            "unit": p.unit,
        }
        for p in products
    ])


@stock_bp.route("/products", methods=["POST"])
@jwt_required()
def post_product():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = product_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    product = create_product(org_id, data)
    return jsonify({"id": product.id, "name": product.name}), 201


@stock_bp.route("/products/<product_id>", methods=["PATCH"])
@jwt_required()
def patch_product(product_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    product = get_product(org_id, product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    try:
        data = product_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    product = update_product_svc(product, data)
    return jsonify({"id": product.id, "name": product.name})


@stock_bp.route("/products/<product_id>", methods=["DELETE"])
@jwt_required()
def delete_product_route(product_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    product = get_product(org_id, product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    delete_product_svc(product)
    return "", 204


@stock_bp.route("/movements", methods=["GET"])
@jwt_required()
def get_movements():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    product_id = request.args.get("product_id")
    movements = list_stock_movements(org_id, product_id=product_id)
    return jsonify([{
        "id": m.id, "date": str(m.date), "product_id": m.product_id, "description": m.description,
        "quantity": float(m.quantity), "price": float(m.price or 0), "movement_type": m.movement_type,
    } for m in movements])


@stock_bp.route("/movements", methods=["POST"])
@jwt_required()
def post_movement():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = movement_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    movement = create_stock_movement(org_id, data)
    return jsonify({"id": movement.id, "date": str(movement.date)}), 201


@stock_bp.route("/movements/<movement_id>", methods=["PATCH"])
@jwt_required()
def patch_movement(movement_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    movement = get_stock_movement(org_id, movement_id)
    if not movement:
        return jsonify({"message": "Movement not found"}), 404
    try:
        data = movement_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    movement = update_stock_movement(movement, data)
    return jsonify({"id": movement.id, "date": str(movement.date)})


@stock_bp.route("/movements/<movement_id>", methods=["DELETE"])
@jwt_required()
def delete_movement_route(movement_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    movement = get_stock_movement(org_id, movement_id)
    if not movement:
        return jsonify({"message": "Movement not found"}), 404
    delete_stock_movement(movement)
    return "", 204


@stock_bp.route("/alerts", methods=["GET"])
@jwt_required()
def alerts():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    threshold = request.args.get("threshold", type=float, default=0)
    alerts_list = get_low_stock_alerts(org_id, threshold=threshold)
    return jsonify(alerts_list)
