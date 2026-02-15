from marshmallow import Schema, fields, validate


class CitySchema(Schema):
    id = fields.Str(dump_only=True)
    organisation_id = fields.Str(dump_only=True)
    name = fields.Str()
    prefecture = fields.Str(allow_none=True)


class CityCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=255))
    prefecture = fields.Str(allow_none=True, validate=validate.Length(max=255))


class CityUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(max=255))
    prefecture = fields.Str(allow_none=True, validate=validate.Length(max=255))
