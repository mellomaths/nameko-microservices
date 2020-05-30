from datetime import datetime

from marshmallow import Schema, fields


class ProductSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    department = fields.String(required=True)
    price = fields.Float(required=True)
    in_stock = fields.Boolean(required=True, default=True)
    created_at = fields.DateTime(default=datetime.now())
