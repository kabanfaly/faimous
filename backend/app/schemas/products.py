from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    id = fields.Str(dump_only=True)
    organisation_id = fields.Str(dump_only=True)
    name = fields.Str()
    description = fields.Str(allow_none=True)
    type = fields.Str(allow_none=True)
    unit = fields.Str(allow_none=True)


class ProductCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=255))
    description = fields.Str(allow_none=True)
    type = fields.Str(allow_none=True, validate=validate.Length(max=50))
    unit = fields.Str(allow_none=True, validate=validate.Length(max=50))


class ProductUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(max=255))
    description = fields.Str(allow_none=True)
    type = fields.Str(allow_none=True, validate=validate.Length(max=50))
    unit = fields.Str(allow_none=True, validate=validate.Length(max=50))
