from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.wholesalers_service import (
    list_wholesalers,
    create_wholesaler,
    get_wholesaler,
    update_wholesaler,
    delete_wholesaler,
)
from app.schemas.wholesalers import WholesalerSchema, WholesalerCreateSchema, WholesalerUpdateSchema

wholesalers_bp = Blueprint("wholesalers", __name__)
wholesaler_schema = WholesalerSchema()
wholesaler_create_schema = WholesalerCreateSchema()
wholesaler_update_schema = WholesalerUpdateSchema()


@wholesalers_bp.route("", methods=["GET"])
@jwt_required()
def get_wholesalers_list():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    wholesalers = list_wholesalers(org_id)
    return jsonify([wholesaler_schema.dump(w) for w in wholesalers])


@wholesalers_bp.route("", methods=["POST"])
@jwt_required()
def post_wholesaler():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = wholesaler_create_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    wholesaler = create_wholesaler(org_id, data)
    return jsonify(wholesaler_schema.dump(wholesaler)), 201


@wholesalers_bp.route("/<wholesaler_id>", methods=["GET"])
@jwt_required()
def get_wholesaler_by_id(wholesaler_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    wholesaler = get_wholesaler(org_id, wholesaler_id)
    if not wholesaler:
        return jsonify({"message": "Wholesaler not found"}), 404
    return jsonify(wholesaler_schema.dump(wholesaler))


@wholesalers_bp.route("/<wholesaler_id>", methods=["PATCH"])
@jwt_required()
def patch_wholesaler(wholesaler_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    wholesaler = get_wholesaler(org_id, wholesaler_id)
    if not wholesaler:
        return jsonify({"message": "Wholesaler not found"}), 404
    try:
        data = wholesaler_update_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    wholesaler = update_wholesaler(wholesaler, data)
    return jsonify(wholesaler_schema.dump(wholesaler))


@wholesalers_bp.route("/<wholesaler_id>", methods=["DELETE"])
@jwt_required()
def remove_wholesaler(wholesaler_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    wholesaler = get_wholesaler(org_id, wholesaler_id)
    if not wholesaler:
        return jsonify({"message": "Wholesaler not found"}), 404
    delete_wholesaler(wholesaler)
    return "", 204
