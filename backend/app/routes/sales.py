from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.sales_service import (
    create_sale as create_sale_svc,
    add_payment_received,
    get_unpaid_sales,
    get_sale,
    update_sale,
    delete_sale,
)
from app.schemas.sales import SaleSchema, PaymentReceivedSchema

sales_bp = Blueprint("sales", __name__)
sale_schema = SaleSchema()
payment_schema = PaymentReceivedSchema()


@sales_bp.route("", methods=["POST"])
@jwt_required()
def create_sale():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = sale_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    sale = create_sale_svc(org_id, data)
    return jsonify({"id": sale.id, "date": str(sale.date)}), 201


@sales_bp.route("/payment", methods=["POST"])
@jwt_required()
def add_payment():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = payment_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    payment = add_payment_received(data["sale_id"], org_id, data)
    if not payment:
        return jsonify({"message": "Sale not found"}), 404
    return jsonify({"id": payment.id}), 201


@sales_bp.route("/unpaid", methods=["GET"])
@jwt_required()
def unpaid():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    sales = get_unpaid_sales(org_id)
    return jsonify([{"id": s.id, "date": str(s.date), "total_price": float(s.total_price or 0), "payment_status": s.payment_status} for s in sales])


@sales_bp.route("/<sale_id>", methods=["GET"])
@jwt_required()
def get_sale_route(sale_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    sale = get_sale(org_id, sale_id)
    if not sale:
        return jsonify({"message": "Sale not found"}), 404
    return jsonify({
        "id": sale.id, "date": str(sale.date), "quantity": sale.quantity or 0,
        "unit_price": float(sale.unit_price or 0), "total_price": float(sale.total_price or 0),
        "payment_status": sale.payment_status,
    })


@sales_bp.route("/<sale_id>", methods=["PATCH"])
@jwt_required()
def patch_sale(sale_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    sale = get_sale(org_id, sale_id)
    if not sale:
        return jsonify({"message": "Sale not found"}), 404
    try:
        data = sale_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    sale = update_sale(sale, data)
    return jsonify({"id": sale.id, "date": str(sale.date)})


@sales_bp.route("/<sale_id>", methods=["DELETE"])
@jwt_required()
def delete_sale_route(sale_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    sale = get_sale(org_id, sale_id)
    if not sale:
        return jsonify({"message": "Sale not found"}), 404
    delete_sale(sale)
    return "", 204
