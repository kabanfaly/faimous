from marshmallow import Schema, fields, validate


class EggProductionSchema(Schema):
    date = fields.Date(required=True)
    eggs_count = fields.Int(load_default=0)
    broken_count = fields.Int(load_default=0)
    trays = fields.Int(allow_none=True)
    remaining = fields.Int(allow_none=True)
    note = fields.Str(allow_none=True)
    farm_id = fields.Str(allow_none=True)


class FlockRecordSchema(Schema):
    date = fields.Date(required=True)
    total_hens = fields.Int(load_default=0)
    dead = fields.Int(load_default=0)
    note = fields.Str(allow_none=True)
    farm_id = fields.Str(allow_none=True)


class DailyOperationSchema(Schema):
    date = fields.Date(required=True)
    period = fields.Str(allow_none=True)
    collect1 = fields.Int(allow_none=True)
    collect2 = fields.Int(allow_none=True)
    collect3 = fields.Int(allow_none=True)
    collect4 = fields.Int(allow_none=True)
    broken = fields.Int(allow_none=True)
    hens = fields.Int(allow_none=True)
    dead = fields.Int(allow_none=True)
    farm_id = fields.Str(allow_none=True)
