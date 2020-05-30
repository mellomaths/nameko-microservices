from mongoengine import Document, StringField, FloatField, BooleanField, DateTimeField

from datetime import datetime


class Product(Document):
    title = StringField(required=True, max_length=200)
    description = StringField(required=True, max_length=200)
    department = StringField(required=True, max_length=200)
    price = FloatField(required=True)
    in_stock = BooleanField(required=True, default=True)
    created_at = DateTimeField(required=True, default=datetime.utcnow())
