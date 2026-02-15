from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import User, Organisation
from app.schemas.auth import OrganisationSchema

organisations_bp = Blueprint("organisations", __name__)
organisation_schema = OrganisationSchema()


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
