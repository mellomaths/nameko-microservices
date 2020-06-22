from marshmallow import Schema, fields


class ProductSchema(Schema):
    id = fields.Integer()
    order_id = fields.Integer()
    serial_number = fields.String()
    title = fields.String()
    description = fields.String()
    price = fields.String()
    quantity = fields.String()


class OrderSchema(Schema):
    id = fields.Integer()
    products = fields.List(fields.Nested(ProductSchema))
    total_price = fields.Float()
    created_at = fields.String()
