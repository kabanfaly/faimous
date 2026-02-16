from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.constants.currencies import get_currencies_list

currencies_bp = Blueprint("currencies", __name__)


@currencies_bp.route("", methods=["GET"])
@jwt_required()
def list_currencies():
    """Return supported currencies (code, symbol, name)."""
    return jsonify(get_currencies_list())
