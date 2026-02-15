from marshmallow import Schema, fields


class ContributionSchema(Schema):
    date = fields.Date(required=True)
    shareholder_id = fields.Str(allow_none=True)
    amount = fields.Decimal(required=True, as_string=True)
    currency = fields.Str(allow_none=True)
    amount_base = fields.Decimal(allow_none=True, as_string=True)
    description = fields.Str(allow_none=True)
