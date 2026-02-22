from marshmallow import Schema, fields


class SaleSchema(Schema):
    date = fields.Date(required=True)
    farm_id = fields.Str(allow_none=True)
    type = fields.Str(allow_none=True)
    quantity = fields.Int(load_default=0)
    unit_price = fields.Decimal(allow_none=True, as_string=True)
    total_price = fields.Decimal(allow_none=True, as_string=True)
    theoretical_price = fields.Decimal(allow_none=True, as_string=True)
    price_diff = fields.Decimal(allow_none=True, as_string=True)
    wholesaler_id = fields.Str(allow_none=True)
    payment_status = fields.Str(load_default="unpaid")
    currency = fields.Str(allow_none=True)
    amount_base = fields.Decimal(allow_none=True, as_string=True)


class PaymentReceivedSchema(Schema):
    sale_id = fields.Str(required=True)
    date = fields.Date(required=True)
    amount = fields.Decimal(required=True, as_string=True)
    payment_method = fields.Str(allow_none=True)
    note = fields.Str(allow_none=True)
