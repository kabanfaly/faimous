from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

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
    farms = list_farms()
    return jsonify([farm_schema.dump(f) for f in farms])


@farms_bp.route("", methods=["POST"])
@jwt_required()
def post_farm():
    try:
        data = farm_create_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    farm = create_farm(data)
    return jsonify(farm_schema.dump(farm)), 201


@farms_bp.route("/<farm_id>", methods=["GET"])
@jwt_required()
def get_farm_by_id(farm_id):
    farm = get_farm(farm_id)
    if not farm:
        return jsonify({"message": "Farm not found"}), 404
    return jsonify(farm_schema.dump(farm))


@farms_bp.route("/<farm_id>", methods=["PATCH"])
@jwt_required()
def patch_farm(farm_id):
    farm = get_farm(farm_id)
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
    farm = get_farm(farm_id)
    if not farm:
        return jsonify({"message": "Farm not found"}), 404
    delete_farm(farm)
    return "", 204
