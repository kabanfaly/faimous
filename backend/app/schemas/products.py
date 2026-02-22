from marshmallow import Schema, fields, validate

from app.schemas.farms import FarmSchema


class ProductTypeSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    farm_id = fields.Str(required=True)
    farm = fields.Nested(FarmSchema, allow_none=True, dump_only=True)


class ProductTypeCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=50))
    farm_id = fields.Str(required=True)


class ProductTypeUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(max=50))
    farm_id = fields.Str()  # optional for partial update, but must be non-null if provided


class ProductSchema(Schema):
    id = fields.Str(dump_only=True)
    product_type_id = fields.Str()
    product_type = fields.Nested(ProductTypeSchema, allow_none=True, dump_only=True)
    name = fields.Str()
    description = fields.Str(allow_none=True)
    unit = fields.Str(allow_none=True)


class ProductCreateSchema(Schema):
    product_type_id = fields.Str(required=True)
    name = fields.Str(required=True, validate=validate.Length(max=255))
    description = fields.Str(allow_none=True)
    unit = fields.Str(allow_none=True, validate=validate.Length(max=50))


class ProductUpdateSchema(Schema):
    product_type_id = fields.Str()
    name = fields.Str(validate=validate.Length(max=255))
    description = fields.Str(allow_none=True)
    unit = fields.Str(allow_none=True, validate=validate.Length(max=50))
