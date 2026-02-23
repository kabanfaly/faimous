from marshmallow import Schema, fields


class ProductTypeSchema(Schema):
    id = fields.Str()
    name = fields.Str()


class ProductSchema(Schema):
    name = fields.Str(required=True)
    product_type_id = fields.Str(required=True)
    product_type = fields.Nested(ProductTypeSchema, allow_none=True)
    description = fields.Str(allow_none=True)
    quantity = fields.Decimal(allow_none=True, as_string=True)
    unit = fields.Str(allow_none=True)


class StockMovementSchema(Schema):
    date = fields.Date(required=True)
    product_id = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    quantity = fields.Decimal(required=True, as_string=True)
    price = fields.Decimal(allow_none=True, as_string=True)
    movement_type = fields.Str(allow_none=True)
    purchase_id = fields.Str(allow_none=True)
