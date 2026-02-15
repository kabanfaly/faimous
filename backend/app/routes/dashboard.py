from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.multi_tenant.context import get_current_organisation_id
from app.services.dashboard_service import get_dashboard_summary, get_dashboard_charts

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    data = get_dashboard_summary(org_id)
    return jsonify(data)


@dashboard_bp.route("/charts", methods=["GET"])
@jwt_required()
def charts():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    data = get_dashboard_charts(org_id)
    return jsonify(data)
