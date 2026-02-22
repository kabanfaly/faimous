from marshmallow import Schema, fields, validate


class WholesalerSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    city_id = fields.Str(allow_none=True)


class WholesalerCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=255))
    city_id = fields.Str(allow_none=True)


class WholesalerUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(max=255))
    city_id = fields.Str(allow_none=True)
