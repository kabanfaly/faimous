from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app import db
from app.schemas.products import (
    ProductTypeSchema,
    ProductTypeCreateSchema,
    ProductTypeUpdateSchema,
)
from app.services.product_types_service import (
    list_product_types,
    create_product_type,
    get_product_type,
    update_product_type,
    delete_product_type,
)

product_types_bp = Blueprint("product_types", __name__)
product_type_schema = ProductTypeSchema()


@product_types_bp.route("", methods=["GET"])
@jwt_required()
def get_product_types_list():
    types = list_product_types()
    return jsonify([product_type_schema.dump(t) for t in types])


@product_types_bp.route("", methods=["POST"])
@jwt_required()
def post_product_type():
    try:
        data = ProductTypeCreateSchema().load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    try:
        pt = create_product_type(data)
        return jsonify(product_type_schema.dump(pt)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Product type with this name already exists"}), 409


@product_types_bp.route("/<product_type_id>", methods=["GET"])
@jwt_required()
def get_product_type_by_id(product_type_id):
    pt = get_product_type(product_type_id)
    if not pt:
        return jsonify({"message": "Product type not found"}), 404
    return jsonify(product_type_schema.dump(pt))


@product_types_bp.route("/<product_type_id>", methods=["PATCH"])
@jwt_required()
def patch_product_type(product_type_id):
    pt = get_product_type(product_type_id)
    if not pt:
        return jsonify({"message": "Product type not found"}), 404
    try:
        data = ProductTypeUpdateSchema().load(request.get_json() or {}, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    try:
        pt = update_product_type(pt, data)
        return jsonify(product_type_schema.dump(pt))
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Product type with this name already exists"}), 409


@product_types_bp.route("/<product_type_id>", methods=["DELETE"])
@jwt_required()
def remove_product_type(product_type_id):
    pt = get_product_type(product_type_id)
    if not pt:
        return jsonify({"message": "Product type not found"}), 404
    try:
        delete_product_type(pt)
        return "", 204
    except ValueError as e:
        return jsonify({"message": str(e)}), 409
