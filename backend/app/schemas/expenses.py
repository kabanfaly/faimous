from marshmallow import Schema, fields


class ExpenseCategorySchema(Schema):
    name = fields.Str(required=True)


class ExpenseSchema(Schema):
    date = fields.Date(required=True)
    description = fields.Str(allow_none=True)
    category_id = fields.Str(allow_none=True)
    amount = fields.Decimal(required=True, as_string=True)
    currency = fields.Str(allow_none=True)
    amount_base = fields.Decimal(allow_none=True, as_string=True)
    invoice_file = fields.Str(allow_none=True)
    payment_method = fields.Str(allow_none=True)
