from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.suppliers_service import list_suppliers, create_supplier, get_supplier, update_supplier, delete_supplier
from app.schemas.suppliers import SupplierSchema, SupplierCreateSchema, SupplierUpdateSchema

suppliers_bp = Blueprint("suppliers", __name__)
supplier_schema = SupplierSchema()
supplier_create_schema = SupplierCreateSchema()
supplier_update_schema = SupplierUpdateSchema()


@suppliers_bp.route("", methods=["GET"])
@jwt_required()
def get_suppliers():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    suppliers = list_suppliers(org_id)
    return jsonify([supplier_schema.dump(s) for s in suppliers])


@suppliers_bp.route("", methods=["POST"])
@jwt_required()
def post_supplier():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = supplier_create_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    supplier = create_supplier(org_id, data)
    return jsonify(supplier_schema.dump(supplier)), 201


@suppliers_bp.route("/<supplier_id>", methods=["GET"])
@jwt_required()
def get_supplier_by_id(supplier_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    supplier = get_supplier(org_id, supplier_id)
    if not supplier:
        return jsonify({"message": "Supplier not found"}), 404
    return jsonify(supplier_schema.dump(supplier))


@suppliers_bp.route("/<supplier_id>", methods=["PATCH"])
@jwt_required()
def patch_supplier(supplier_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    supplier = get_supplier(org_id, supplier_id)
    if not supplier:
        return jsonify({"message": "Supplier not found"}), 404
    try:
        data = supplier_update_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    supplier = update_supplier(supplier, data)
    return jsonify(supplier_schema.dump(supplier))


@suppliers_bp.route("/<supplier_id>", methods=["DELETE"])
@jwt_required()
def remove_supplier(supplier_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    supplier = get_supplier(org_id, supplier_id)
    if not supplier:
        return jsonify({"message": "Supplier not found"}), 404
    delete_supplier(supplier)
    return "", 204
