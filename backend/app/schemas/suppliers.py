from marshmallow import Schema, fields, validate


class SupplierSchema(Schema):
    id = fields.Str(dump_only=True)
    organisation_id = fields.Str(dump_only=True)
    name = fields.Str()
    phone = fields.Str(allow_none=True)
    email = fields.Email(allow_none=True)
    city_id = fields.Str(allow_none=True)


class SupplierCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=255))
    phone = fields.Str(allow_none=True, validate=validate.Length(max=50))
    email = fields.Email(allow_none=True)
    city_id = fields.Str(allow_none=True)


class SupplierUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(max=255))
    phone = fields.Str(allow_none=True, validate=validate.Length(max=50))
    email = fields.Email(allow_none=True)
    city_id = fields.Str(allow_none=True)
