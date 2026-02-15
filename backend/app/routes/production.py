from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.production_service import (
    create_egg_production,
    create_flock_record,
    create_daily_operation,
    get_production_kpis,
)
from app.schemas.production import EggProductionSchema, FlockRecordSchema, DailyOperationSchema

production_bp = Blueprint("production", __name__)
egg_schema = EggProductionSchema()
flock_schema = FlockRecordSchema()
daily_schema = DailyOperationSchema()


@production_bp.route("/eggs", methods=["POST"])
@jwt_required()
def create_eggs():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = egg_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    rec = create_egg_production(org_id, data)
    return jsonify({"id": rec.id, "date": str(rec.date)}), 201


@production_bp.route("/flock", methods=["POST"])
@jwt_required()
def create_flock():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = flock_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    rec = create_flock_record(org_id, data)
    return jsonify({"id": rec.id, "date": str(rec.date)}), 201


@production_bp.route("/daily", methods=["POST"])
@jwt_required()
def create_daily():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = daily_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    rec = create_daily_operation(org_id, data)
    return jsonify({"id": rec.id, "date": str(rec.date)}), 201


@production_bp.route("/kpis", methods=["GET"])
@jwt_required()
def kpis():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    kpis_data = get_production_kpis(org_id)
    return jsonify(kpis_data)
