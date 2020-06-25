from marshmallow import Schema, fields


class ProductSchema(Schema):
    id = fields.String(required=True, dump_only=True, attribute='product_id')
    product_id = fields.String(required=True, load_only=True)
    amount = fields.String(required=True)
    price = fields.Float(required=True)


class CartSchema(Schema):
    id = fields.String(required=True)
    total_price = fields.Float(required=True, default=0)
    products = fields.List(fields.Nested(ProductSchema), required=True, default=[])
