from marshmallow import Schema, fields, validate


class ShareholderSchema(Schema):
    id = fields.Str(dump_only=True)
    organisation_id = fields.Str(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    phone = fields.Str(allow_none=True)
    email = fields.Email(allow_none=True)


class ShareholderCreateSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(max=100))
    last_name = fields.Str(required=True, validate=validate.Length(max=100))
    phone = fields.Str(allow_none=True, validate=validate.Length(max=50))
    email = fields.Email(allow_none=True)


class ShareholderUpdateSchema(Schema):
    first_name = fields.Str(validate=validate.Length(max=100))
    last_name = fields.Str(validate=validate.Length(max=100))
    phone = fields.Str(allow_none=True, validate=validate.Length(max=50))
    email = fields.Email(allow_none=True)
