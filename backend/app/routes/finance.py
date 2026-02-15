from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.multi_tenant.context import get_current_organisation_id
from app.services.finance_service import get_finance_result, get_cashflow

finance_bp = Blueprint("finance", __name__)


@finance_bp.route("/result", methods=["GET"])
@jwt_required()
def result():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    data = get_finance_result(org_id)
    return jsonify(data)


@finance_bp.route("/cashflow", methods=["GET"])
@jwt_required()
def cashflow():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    from datetime import datetime
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    fd = datetime.strptime(from_date, "%Y-%m-%d").date() if from_date else None
    td = datetime.strptime(to_date, "%Y-%m-%d").date() if to_date else None
    data = get_cashflow(org_id, from_date=fd, to_date=td)
    return jsonify(data)
