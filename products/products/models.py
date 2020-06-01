from mongoengine import Document, StringField, FloatField, IntField, BooleanField, DateTimeField, queryset_manager

from datetime import datetime


class Product(Document):
    title = StringField(required=True, max_length=200)
    description = StringField(required=True, max_length=200)
    department = StringField(required=True, max_length=200)
    price = FloatField(required=True)
    quantity = IntField(required=True)
    created_at = DateTimeField(required=True, default=datetime.utcnow())

    @queryset_manager
    def products_in_stock(self, clazz, queryset):
        return queryset.filter(quantity__gt=0)
