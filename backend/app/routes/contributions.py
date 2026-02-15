from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.contributions_service import (
    list_contributions,
    create_contribution,
    get_contribution,
    update_contribution,
    delete_contribution,
    list_shareholders,
    create_shareholder,
)
from app.services.shareholders_service import get_shareholder, update_shareholder, delete_shareholder
from app.schemas.contributions import ContributionSchema

contributions_bp = Blueprint("contributions", __name__)
contribution_schema = ContributionSchema()


@contributions_bp.route("/shareholders", methods=["GET"])
@jwt_required()
def get_shareholders():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    shareholders = list_shareholders(org_id)
    return jsonify([{"id": s.id, "first_name": s.first_name, "last_name": s.last_name, "phone": s.phone, "email": s.email} for s in shareholders])


@contributions_bp.route("/shareholders", methods=["POST"])
@jwt_required()
def post_shareholder():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    data = request.get_json() or {}
    if not data.get("first_name") or not data.get("last_name"):
        return jsonify({"errors": {"first_name": ["Required"], "last_name": ["Required"]}}), 400
    sh = create_shareholder(org_id, data)
    return jsonify({"id": sh.id, "first_name": sh.first_name, "last_name": sh.last_name}), 201


@contributions_bp.route("/shareholders/<shareholder_id>", methods=["PATCH"])
@jwt_required()
def patch_shareholder(shareholder_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    sh = get_shareholder(org_id, shareholder_id)
    if not sh:
        return jsonify({"message": "Shareholder not found"}), 404
    data = request.get_json() or {}
    sh = update_shareholder(sh, data)
    return jsonify({"id": sh.id, "first_name": sh.first_name, "last_name": sh.last_name})


@contributions_bp.route("/shareholders/<shareholder_id>", methods=["DELETE"])
@jwt_required()
def delete_shareholder_route(shareholder_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    sh = get_shareholder(org_id, shareholder_id)
    if not sh:
        return jsonify({"message": "Shareholder not found"}), 404
    delete_shareholder(sh)
    return "", 204


@contributions_bp.route("", methods=["GET"])
@jwt_required()
def get_contributions():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    contributions = list_contributions(org_id)
    return jsonify([{
        "id": c.id, "date": str(c.date), "shareholder_id": c.shareholder_id, "amount": float(c.amount),
        "currency": c.currency, "amount_base": float(c.amount_base or 0), "description": c.description,
    } for c in contributions])


@contributions_bp.route("", methods=["POST"])
@jwt_required()
def post_contribution():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = contribution_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    contrib = create_contribution(org_id, data)
    return jsonify({"id": contrib.id, "date": str(contrib.date)}), 201


@contributions_bp.route("/<contribution_id>", methods=["PATCH"])
@jwt_required()
def patch_contribution(contribution_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    contrib = get_contribution(org_id, contribution_id)
    if not contrib:
        return jsonify({"message": "Contribution not found"}), 404
    try:
        data = contribution_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    contrib = update_contribution(contrib, data)
    return jsonify({"id": contrib.id, "date": str(contrib.date)})


@contributions_bp.route("/<contribution_id>", methods=["DELETE"])
@jwt_required()
def delete_contribution_route(contribution_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    contrib = get_contribution(org_id, contribution_id)
    if not contrib:
        return jsonify({"message": "Contribution not found"}), 404
    delete_contribution(contrib)
    return "", 204
