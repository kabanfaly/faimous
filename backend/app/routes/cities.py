from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.cities_service import (
    list_cities,
    create_city,
    get_city,
    update_city,
    delete_city,
)
from app.schemas.cities import CitySchema, CityCreateSchema, CityUpdateSchema

cities_bp = Blueprint("cities", __name__)
city_schema = CitySchema()
city_create_schema = CityCreateSchema()
city_update_schema = CityUpdateSchema()


@cities_bp.route("", methods=["GET"])
@jwt_required()
def get_cities_list():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    cities = list_cities(org_id)
    return jsonify([city_schema.dump(c) for c in cities])


@cities_bp.route("", methods=["POST"])
@jwt_required()
def post_city():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = city_create_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    city = create_city(org_id, data)
    return jsonify(city_schema.dump(city)), 201


@cities_bp.route("/<city_id>", methods=["GET"])
@jwt_required()
def get_city_by_id(city_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    city = get_city(org_id, city_id)
    if not city:
        return jsonify({"message": "City not found"}), 404
    return jsonify(city_schema.dump(city))


@cities_bp.route("/<city_id>", methods=["PATCH"])
@jwt_required()
def patch_city(city_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    city = get_city(org_id, city_id)
    if not city:
        return jsonify({"message": "City not found"}), 404
    try:
        data = city_update_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    city = update_city(city, data)
    return jsonify(city_schema.dump(city))


@cities_bp.route("/<city_id>", methods=["DELETE"])
@jwt_required()
def remove_city(city_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    city = get_city(org_id, city_id)
    if not city:
        return jsonify({"message": "City not found"}), 404
    delete_city(city)
    return "", 204
