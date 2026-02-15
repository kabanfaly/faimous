from marshmallow import Schema, fields, validate


class UserCreateSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(max=100))
    last_name = fields.Str(required=True, validate=validate.Length(max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    gender = fields.Str(load_default="male", validate=validate.OneOf(["male", "female"]))
    language = fields.Str(load_default="fr")
    role = fields.Str(load_default="user", validate=validate.OneOf(["owner", "admin", "manager", "worker", "user"]))


class UserUpdateSchema(Schema):
    first_name = fields.Str(validate=validate.Length(max=100))
    last_name = fields.Str(validate=validate.Length(max=100))
    gender = fields.Str(validate=validate.OneOf(["male", "female"]))
    language = fields.Str()
    activated = fields.Bool()
    role = fields.Str(validate=validate.OneOf(["owner", "admin", "manager", "worker", "user"]))
