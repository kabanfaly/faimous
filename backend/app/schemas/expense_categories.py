from marshmallow import Schema, fields, validate


class ExpenseCategorySchema(Schema):
    id = fields.Str(dump_only=True)
    organisation_id = fields.Str(dump_only=True)
    name = fields.Str()


class ExpenseCategoryCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=255))


class ExpenseCategoryUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(max=255))
