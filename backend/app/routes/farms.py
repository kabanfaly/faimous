from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.farms_service import (
    list_farms,
    create_farm,
    get_farm,
    update_farm,
    delete_farm,
)
from app.schemas.farms import FarmSchema, FarmCreateSchema, FarmUpdateSchema

farms_bp = Blueprint("farms", __name__)
farm_schema = FarmSchema()
farm_create_schema = FarmCreateSchema()
farm_update_schema = FarmUpdateSchema()


@farms_bp.route("", methods=["GET"])
@jwt_required()
def get_farms_list():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    farms = list_farms(org_id)
    return jsonify([farm_schema.dump(f) for f in farms])


@farms_bp.route("", methods=["POST"])
@jwt_required()
def post_farm():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = farm_create_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    farm = create_farm(org_id, data)
    return jsonify(farm_schema.dump(farm)), 201


@farms_bp.route("/<farm_id>", methods=["GET"])
@jwt_required()
def get_farm_by_id(farm_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    farm = get_farm(org_id, farm_id)
    if not farm:
        return jsonify({"message": "Farm not found"}), 404
    return jsonify(farm_schema.dump(farm))


@farms_bp.route("/<farm_id>", methods=["PATCH"])
@jwt_required()
def patch_farm(farm_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    farm = get_farm(org_id, farm_id)
    if not farm:
        return jsonify({"message": "Farm not found"}), 404
    try:
        data = farm_update_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    farm = update_farm(farm, data)
    return jsonify(farm_schema.dump(farm))


@farms_bp.route("/<farm_id>", methods=["DELETE"])
@jwt_required()
def remove_farm(farm_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    farm = get_farm(org_id, farm_id)
    if not farm:
        return jsonify({"message": "Farm not found"}), 404
    delete_farm(farm)
    return "", 204
