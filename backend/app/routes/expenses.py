from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.expenses_service import (
    list_expense_categories,
    create_expense_category,
    list_expenses,
    create_expense,
    get_expense,
    update_expense,
    delete_expense,
)
from app.schemas.expenses import ExpenseCategorySchema, ExpenseSchema

expenses_bp = Blueprint("expenses", __name__)
category_schema = ExpenseCategorySchema()
expense_schema = ExpenseSchema()


@expenses_bp.route("/categories", methods=["GET"])
@jwt_required()
def get_categories():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    categories = list_expense_categories(org_id)
    return jsonify([{"id": c.id, "name": c.name} for c in categories])


@expenses_bp.route("/categories", methods=["POST"])
@jwt_required()
def post_category():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = category_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    cat = create_expense_category(org_id, data)
    return jsonify({"id": cat.id, "name": cat.name}), 201


@expenses_bp.route("", methods=["GET"])
@jwt_required()
def get_expenses():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    expenses = list_expenses(org_id)
    return jsonify([{
        "id": e.id, "date": str(e.date), "description": e.description, "farm_id": e.farm_id,
        "category_id": e.category_id, "amount": float(e.amount), "currency": e.currency,
        "amount_base": float(e.amount_base or 0),
    } for e in expenses])


@expenses_bp.route("", methods=["POST"])
@jwt_required()
def post_expense():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = expense_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    expense = create_expense(org_id, data)
    return jsonify({"id": expense.id, "date": str(expense.date)}), 201


@expenses_bp.route("/<expense_id>", methods=["PATCH"])
@jwt_required()
def patch_expense(expense_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    expense = get_expense(org_id, expense_id)
    if not expense:
        return jsonify({"message": "Expense not found"}), 404
    try:
        data = expense_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    expense = update_expense(expense, data)
    return jsonify({"id": expense.id, "date": str(expense.date)})


@expenses_bp.route("/<expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense_route(expense_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    expense = get_expense(org_id, expense_id)
    if not expense:
        return jsonify({"message": "Expense not found"}), 404
    delete_expense(expense)
    return "", 204
