from marshmallow import Schema, fields, validate


class FarmSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    city_id = fields.Str(allow_none=True)


class FarmCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=255))
    city_id = fields.Str(allow_none=True)


class FarmUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(max=255))
    city_id = fields.Str(allow_none=True)
