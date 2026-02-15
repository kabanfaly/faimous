from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.users_service import list_users, create_user, get_user, update_user
from app.schemas.auth import UserSchema
from app.schemas.users import UserCreateSchema, UserUpdateSchema

users_bp = Blueprint("users", __name__)
user_schema = UserSchema()
user_create_schema = UserCreateSchema()
user_update_schema = UserUpdateSchema()


def _require_admin():
    claims = get_jwt()
    role = claims.get("role")
    if role not in ("owner", "admin"):
        return False
    return True


@users_bp.route("", methods=["GET"])
@jwt_required()
def get_users():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    if not _require_admin():
        return jsonify({"message": "Admin or owner required"}), 403
    users = list_users(org_id)
    return jsonify([user_schema.dump(u) for u in users])


@users_bp.route("", methods=["POST"])
@jwt_required()
def post_user():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    if not _require_admin():
        return jsonify({"message": "Admin or owner required"}), 403
    try:
        data = user_create_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    user, err = create_user(org_id, data)
    if err:
        return jsonify({"message": err}), 409
    return jsonify(user_schema.dump(user)), 201


@users_bp.route("/<user_id>", methods=["GET"])
@jwt_required()
def get_user_by_id(user_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    user = get_user(org_id, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user_schema.dump(user))


@users_bp.route("/<user_id>", methods=["PATCH"])
@jwt_required()
def patch_user(user_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    if not _require_admin():
        return jsonify({"message": "Admin or owner required"}), 403
    user = get_user(org_id, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    try:
        data = user_update_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    user = update_user(user, data)
    return jsonify(user_schema.dump(user))
