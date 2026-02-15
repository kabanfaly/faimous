from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.shareholders_service import (
    list_shareholders,
    create_shareholder,
    get_shareholder,
    update_shareholder,
    delete_shareholder,
)
from app.schemas.shareholders import ShareholderSchema, ShareholderCreateSchema, ShareholderUpdateSchema

shareholders_bp = Blueprint("shareholders", __name__)
shareholder_schema = ShareholderSchema()
shareholder_create_schema = ShareholderCreateSchema()
shareholder_update_schema = ShareholderUpdateSchema()


@shareholders_bp.route("", methods=["GET"])
@jwt_required()
def get_shareholders_list():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    shareholders = list_shareholders(org_id)
    return jsonify([shareholder_schema.dump(s) for s in shareholders])


@shareholders_bp.route("", methods=["POST"])
@jwt_required()
def post_shareholder():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = shareholder_create_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    shareholder = create_shareholder(org_id, data)
    return jsonify(shareholder_schema.dump(shareholder)), 201


@shareholders_bp.route("/<shareholder_id>", methods=["GET"])
@jwt_required()
def get_shareholder_by_id(shareholder_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    shareholder = get_shareholder(org_id, shareholder_id)
    if not shareholder:
        return jsonify({"message": "Shareholder not found"}), 404
    return jsonify(shareholder_schema.dump(shareholder))


@shareholders_bp.route("/<shareholder_id>", methods=["PATCH"])
@jwt_required()
def patch_shareholder(shareholder_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    shareholder = get_shareholder(org_id, shareholder_id)
    if not shareholder:
        return jsonify({"message": "Shareholder not found"}), 404
    try:
        data = shareholder_update_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    shareholder = update_shareholder(shareholder, data)
    return jsonify(shareholder_schema.dump(shareholder))


@shareholders_bp.route("/<shareholder_id>", methods=["DELETE"])
@jwt_required()
def remove_shareholder(shareholder_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    shareholder = get_shareholder(org_id, shareholder_id)
    if not shareholder:
        return jsonify({"message": "Shareholder not found"}), 404
    delete_shareholder(shareholder)
    return "", 204
