from marshmallow import Schema, fields, validate


class FarmSchema(Schema):
    id = fields.Str(dump_only=True)
    organisation_id = fields.Str(dump_only=True)
    name = fields.Str()
    location = fields.Str(allow_none=True)


class FarmCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=255))
    location = fields.Str(allow_none=True, validate=validate.Length(max=255))


class FarmUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(max=255))
    location = fields.Str(allow_none=True, validate=validate.Length(max=255))
