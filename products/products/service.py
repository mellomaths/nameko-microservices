import os
from bson.objectid import ObjectId

from nameko.rpc import rpc
from nameko_structlog import StructlogDependency

from mongoengine import connect, DoesNotExist

from marshmallow import ValidationError

from .models import Product
from .schemas import ProductSchema


class ProductsService(object):
    name = 'products'
    log = StructlogDependency()

    mongodb_user = os.getenv('MONGODB_USER') or 'system'
    mongodb_password = os.getenv('MONGODB_PASSWORD') or 'system'
    mongodb_host = os.getenv('MONGODB_HOST') or 'localhost'
    mongodb_port = os.getenv('MONGODB_PORT') or '27017'
    mongodb_db_name = os.getenv('MONGODB_DB_NAME') or 'products'
    mongodb_authentication_base = os.getenv('MONGODB_AUTHENTICATION_BASE') or 'admin'

    connect(
        'products',
        username=mongodb_user,
        password=mongodb_password,
        host=mongodb_host,
        port=int(mongodb_port),
        authentication_source=mongodb_authentication_base
    )

    @rpc
    def health_check(self):
        self.log.info(f'products.home:: start')
        response = 'Products service is up and running!'
        self.log.info(f'products.home:: response {response}')
        self.log.info(f'products.home:: end')
        return response

    @rpc
    def create(self, data):
        self.log.info(f'products.create:: start')
        self.log.info(f'products.create:: data {data}')
        schema = ProductSchema()
        try:
            data = schema.load(data)
        except ValidationError as err:
            self.log.info(f'products.create:: validation error {err}')
            error_response = {
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'description': 'Validation Error',
                    'validations': err.messages
                }
            }
            return error_response

        self.log.info(f'products.create:: product loaded {data}')
        product = Product(**data)
        product.save()
        self.log.info(f'products.create:: product {product}')
        self.log.info(f'products.create:: end')
        return {'id': str(product.id)}

    @rpc
    def show(self, product_id):
        self.log.info(f'products.show:: start')
        self.log.info(f'products.show:: product id {product_id}')

        try:
            product = Product.objects.get(id=ObjectId(product_id))
        except DoesNotExist as err:
            self.log.info(f'products.show:: product not found')
            self.log.info(f'products.show:: exception {err}')
            self.log.info(f'products.show:: end')
            return None

        self.log.info(f'products.show:: query result {product}')
        self.log.info(f'products.show:: end')
        return ProductSchema().dump(product)

    @rpc
    def list(self):
        self.log.info(f'products.list:: start')
        product_list = list(Product.objects)
        self.log.info(f'products.list:: query result {product_list}')
        self.log.info(f'products.create:: end')
        return ProductSchema().dump(product_list, many=True)

    @rpc
    def decrement_stock(self, product_id, amount):
        self.log.info(f'products.decrement_stock:: start')
        self.log.info(f'products.decrement_stock:: product id {product_id}')
        self.log.info(f'products.decrement_stock:: amount {amount}')
        try:
            product = Product.objects.get(id=ObjectId(product_id))
        except DoesNotExist as err:
            self.log.info(f'products.decrement_stock:: product not found')
            self.log.info(f'products.decrement_stock:: exception {err}')
            self.log.info(f'products.decrement_stock:: end')
            return None

        if product.quantity == 0:
            self.log.info(f'products.decrement_stock:: there is no product {product_id} in stock')
            error_response = {
                'error': {
                    'code': 'NOT_FOUND_IN_STOCK',
                    'description': 'Quantity in stock for product cannot go lower than 0.'
                }
            }
            self.log.info(f'products.decrement_stock:: error response {error_response}')
            return error_response

        self.log.info(f'products.decrement_stock:: product {product_id} quantity in stock before {product.quantity}')
        product.quantity -= amount
        self.log.info(f'products.decrement_stock:: product {product_id} quantity in stock after {product.quantity}')
        product.save()
        self.log.info(f'products.decrement_stock:: product {product}')
        self.log.info(f'products.decrement_stock:: end')
        return product
