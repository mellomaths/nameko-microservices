from marshmallow import Schema, fields


class ProductSchema(Schema):
    id = fields.String(required=True)
    amount = fields.String(required=True)


class CartSchema(Schema):
    id = fields.String(required=True)
    products = fields.List(fields.Nested(ProductSchema), required=True)


# Cart
# {
#     "products": [
#         {
#             'id': 18743,
#             'amount': 2
#         },
#         {
#             'id': 27232,
#             'amount': 1
#         },
#         {
#             'id': 129023,
#             'amount': 10
#         }
#     ]
# }
