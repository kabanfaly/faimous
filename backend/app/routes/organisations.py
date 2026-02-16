from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from marshmallow import ValidationError

from app import db
from app.models import User, Organisation
from app.schemas.auth import OrganisationSchema, OrganisationUpdateSchema

organisations_bp = Blueprint("organisations", __name__)
organisation_schema = OrganisationSchema()
organisation_update_schema = OrganisationUpdateSchema()


def _require_admin():
    claims = get_jwt()
    role = claims.get("role")
    return role in ("owner", "admin")


@organisations_bp.route("/current", methods=["GET"])
@jwt_required()
def current():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    org = Organisation.query.get(user.organisation_id)
    if not org:
        return jsonify({"message": "Organisation not found"}), 404
    return jsonify(organisation_schema.dump(org))


@organisations_bp.route("/current", methods=["PATCH"])
@jwt_required()
def update_current():
    if not _require_admin():
        return jsonify({"message": "Admin or owner required"}), 403
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    org = Organisation.query.get(user.organisation_id)
    if not org:
        return jsonify({"message": "Organisation not found"}), 404
    try:
        data = organisation_update_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    if not data:
        return jsonify(organisation_schema.dump(org))
    if "name" in data:
        org.name = data["name"]
    if "currency_default" in data:
        org.currency_default = data["currency_default"]
    if "language_default" in data:
        org.language_default = data["language_default"]
    db.session.commit()
    return jsonify(organisation_schema.dump(org))
