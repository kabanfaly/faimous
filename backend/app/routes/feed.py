from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.feed_service import (
    list_feed_preparations,
    create_feed_preparation,
    get_feed_preparation,
    update_feed_preparation,
    delete_feed_preparation,
)
from app.schemas.feed import FeedPreparationSchema

feed_bp = Blueprint("feed", __name__)
preparation_schema = FeedPreparationSchema()


@feed_bp.route("/preparations", methods=["GET"])
@jwt_required()
def get_preparations():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    preparations = list_feed_preparations(org_id)
    return jsonify([{
        "id": p.id, "date": str(p.date), "quantity_kg": float(p.quantity_kg), "ratio": p.ratio,
        "hens_available": p.hens_available, "expected_end_date": str(p.expected_end_date) if p.expected_end_date else None,
        "note": p.note,
    } for p in preparations])


@feed_bp.route("/preparations", methods=["POST"])
@jwt_required()
def post_preparation():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = preparation_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    prep = create_feed_preparation(org_id, data)
    return jsonify({"id": prep.id, "date": str(prep.date)}), 201


@feed_bp.route("/preparations/<prep_id>", methods=["PATCH"])
@jwt_required()
def patch_preparation(prep_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    prep = get_feed_preparation(org_id, prep_id)
    if not prep:
        return jsonify({"message": "Preparation not found"}), 404
    try:
        data = preparation_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    prep = update_feed_preparation(prep, data)
    return jsonify({"id": prep.id, "date": str(prep.date)})


@feed_bp.route("/preparations/<prep_id>", methods=["DELETE"])
@jwt_required()
def delete_preparation_route(prep_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    prep = get_feed_preparation(org_id, prep_id)
    if not prep:
        return jsonify({"message": "Preparation not found"}), 404
    delete_feed_preparation(prep)
    return "", 204
