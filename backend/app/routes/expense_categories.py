from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.expense_categories_service import (
    list_expense_categories,
    create_expense_category,
    get_expense_category,
    update_expense_category,
    delete_expense_category,
)
from app.schemas.expense_categories import (
    ExpenseCategorySchema,
    ExpenseCategoryCreateSchema,
    ExpenseCategoryUpdateSchema,
)

expense_categories_bp = Blueprint("expense_categories", __name__)
expense_category_schema = ExpenseCategorySchema()
expense_category_create_schema = ExpenseCategoryCreateSchema()
expense_category_update_schema = ExpenseCategoryUpdateSchema()


@expense_categories_bp.route("", methods=["GET"])
@jwt_required()
def get_expense_categories_list():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    categories = list_expense_categories(org_id)
    return jsonify([expense_category_schema.dump(c) for c in categories])


@expense_categories_bp.route("", methods=["POST"])
@jwt_required()
def post_expense_category():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = expense_category_create_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    category = create_expense_category(org_id, data)
    return jsonify(expense_category_schema.dump(category)), 201


@expense_categories_bp.route("/<category_id>", methods=["GET"])
@jwt_required()
def get_expense_category_by_id(category_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    category = get_expense_category(org_id, category_id)
    if not category:
        return jsonify({"message": "Expense category not found"}), 404
    return jsonify(expense_category_schema.dump(category))


@expense_categories_bp.route("/<category_id>", methods=["PATCH"])
@jwt_required()
def patch_expense_category(category_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    category = get_expense_category(org_id, category_id)
    if not category:
        return jsonify({"message": "Expense category not found"}), 404
    try:
        data = expense_category_update_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    category = update_expense_category(category, data)
    return jsonify(expense_category_schema.dump(category))


@expense_categories_bp.route("/<category_id>", methods=["DELETE"])
@jwt_required()
def remove_expense_category(category_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    category = get_expense_category(org_id, category_id)
    if not category:
        return jsonify({"message": "Expense category not found"}), 404
    delete_expense_category(category)
    return "", 204
