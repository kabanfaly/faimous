from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class RegisterSchema(Schema):
    organisation_name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    first_name = fields.Str(load_default="")
    last_name = fields.Str(load_default="")


class UpdateProfileSchema(Schema):
    first_name = fields.Str(validate=validate.Length(max=100))
    last_name = fields.Str(validate=validate.Length(max=100))
    email = fields.Email()


class ChangePasswordSchema(Schema):
    current_password = fields.Str(required=True, load_only=True)
    new_password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    organisation_id = fields.Str(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    gender = fields.Str()
    email = fields.Email()
    language = fields.Str()
    role = fields.Str()
    activated = fields.Bool()


class OrganisationSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    currency_default = fields.Str()
    language_default = fields.Str()
    created_at = fields.DateTime(dump_only=True)
