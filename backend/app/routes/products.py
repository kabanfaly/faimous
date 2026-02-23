from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.multi_tenant.context import get_current_organisation_id
from app.services.products_service import (
    list_products,
    create_product,
    get_product,
    update_product,
    delete_product,
)
from app.schemas.products import ProductSchema, ProductCreateSchema, ProductUpdateSchema

products_bp = Blueprint("products", __name__)
product_schema = ProductSchema()
product_create_schema = ProductCreateSchema()
product_update_schema = ProductUpdateSchema()


@products_bp.route("", methods=["GET"])
@jwt_required()
def get_products_list():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    products = list_products(org_id)
    return jsonify([product_schema.dump(p) for p in products])


@products_bp.route("/units", methods=["GET"])
@jwt_required()
def get_product_units():
    units = current_app.config.get("PRODUCT_UNITS", [])
    return jsonify(units)


@products_bp.route("", methods=["POST"])
@jwt_required()
def post_product():
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    try:
        data = product_create_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    product = create_product(org_id, data)
    return jsonify(product_schema.dump(product)), 201


@products_bp.route("/<product_id>", methods=["GET"])
@jwt_required()
def get_product_by_id(product_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    product = get_product(org_id, product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    return jsonify(product_schema.dump(product))


@products_bp.route("/<product_id>", methods=["PATCH"])
@jwt_required()
def patch_product(product_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    product = get_product(org_id, product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    try:
        data = product_update_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    product = update_product(product, data)
    return jsonify(product_schema.dump(product))


@products_bp.route("/<product_id>", methods=["DELETE"])
@jwt_required()
def remove_product(product_id):
    org_id = get_current_organisation_id()
    if not org_id:
        return jsonify({"message": "Organisation required"}), 403
    product = get_product(org_id, product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    delete_product(product)
    return "", 204
