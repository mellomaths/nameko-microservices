from marshmallow import Schema, fields


class ProductSchema(Schema):
    id = fields.String(dump_only=True, attribute='product_id')
    product_id = fields.String(required=True, load_only=True)
    amount = fields.Integer(required=True)
    price = fields.Float(dump_only=True)


class CartSchema(Schema):
    id = fields.String(required=True)
    total_price = fields.Float(required=True, default=0)
    products = fields.List(fields.Nested(ProductSchema), required=True, default=[])
