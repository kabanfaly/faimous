from marshmallow import Schema, fields


class PurchaseSchema(Schema):
    date = fields.Date(required=True)
    supplier_id = fields.Str(allow_none=True)
    product_id = fields.Str(allow_none=True)
    unit_price = fields.Decimal(allow_none=True, as_string=True)
    quantity = fields.Decimal(load_default=0, as_string=True)
    total_price = fields.Decimal(allow_none=True, as_string=True)
    status = fields.Str(load_default="unpaid")
    currency = fields.Str(allow_none=True)
    amount_base = fields.Decimal(allow_none=True, as_string=True)


class SupplierPaymentSchema(Schema):
    purchase_id = fields.Str(required=True)
    date = fields.Date(required=True)
    amount = fields.Decimal(required=True, as_string=True)
    payment_method = fields.Str(allow_none=True)
    note = fields.Str(allow_none=True)
