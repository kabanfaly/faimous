from marshmallow import Schema, fields


class FeedPreparationSchema(Schema):
    date = fields.Date(required=True)
    quantity_kg = fields.Decimal(required=True, as_string=True)
    ratio = fields.Str(allow_none=True)
    hens_available = fields.Int(allow_none=True)
    expected_end_date = fields.Date(allow_none=True)
    note = fields.Str(allow_none=True)
