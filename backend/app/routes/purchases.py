from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.purchases_service import (
    create_purchase as create_purchase_svc,
    add_supplier_payment,
    get_unpaid_purchases,
    get_purchase,
    update_purchase,
    delete_purchase,
)
from app.schemas.purchases import PurchaseSchema, SupplierPaymentSchema

purchases_bp = Blueprint("purchases", __name__)
purchase_schema = PurchaseSchema()
payment_schema = SupplierPaymentSchema()


@purchases_bp.route("", methods=["POST"])
@jwt_required()
def create_purchase():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = purchase_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    purchase = create_purchase_svc(org_id, data)
    return jsonify({"id": purchase.id, "date": str(purchase.date)}), 201


@purchases_bp.route("/payment", methods=["POST"])
@jwt_required()
def add_payment():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = payment_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    payment = add_supplier_payment(data["purchase_id"], org_id, data)
    if not payment:
        return jsonify({"message": "Purchase not found"}), 404
    return jsonify({"id": payment.id}), 201


@purchases_bp.route("/unpaid", methods=["GET"])
@jwt_required()
def unpaid():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    purchases = get_unpaid_purchases(org_id)
    return jsonify([{"id": p.id, "date": str(p.date), "total_price": float(p.total_price or 0), "status": p.status} for p in purchases])


@purchases_bp.route("/<purchase_id>", methods=["GET"])
@jwt_required()
def get_purchase_route(purchase_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    purchase = get_purchase(org_id, purchase_id)
    if not purchase:
        return jsonify({"message": "Purchase not found"}), 404
    return jsonify({
        "id": purchase.id, "date": str(purchase.date), "supplier_id": purchase.supplier_id,
        "product_id": purchase.product_id, "quantity": float(purchase.quantity or 0),
        "unit_price": float(purchase.unit_price or 0), "total_price": float(purchase.total_price or 0),
        "status": purchase.status,
    })


@purchases_bp.route("/<purchase_id>", methods=["PATCH"])
@jwt_required()
def patch_purchase(purchase_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    purchase = get_purchase(org_id, purchase_id)
    if not purchase:
        return jsonify({"message": "Purchase not found"}), 404
    try:
        data = purchase_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    purchase = update_purchase(purchase, data)
    return jsonify({"id": purchase.id, "date": str(purchase.date)})


@purchases_bp.route("/<purchase_id>", methods=["DELETE"])
@jwt_required()
def delete_purchase_route(purchase_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    purchase = get_purchase(org_id, purchase_id)
    if not purchase:
        return jsonify({"message": "Purchase not found"}), 404
    delete_purchase(purchase)
    return "", 204
