from bson.objectid import ObjectId

from marshmallow import Schema, fields, ValidationError, pre_load

Schema.TYPE_MAPPING[ObjectId] = fields.String


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided. Field should not be blank.')


class ProductSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=must_not_be_blank)
    description = fields.String(required=True, validate=must_not_be_blank)
    department = fields.String(required=True, validate=must_not_be_blank)
    price = fields.Float(required=True)
    in_stock = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        datetimeformat = '%Y-%m-%dT%H:%M:%S-03:00'
