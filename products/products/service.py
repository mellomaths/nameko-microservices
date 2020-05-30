import os

from nameko.rpc import rpc

from nameko_structlog import StructlogDependency

from pymongo import MongoClient

from marshmallow import ValidationError

from bson.objectid import ObjectId

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

    connect_uri = f'mongodb://{mongodb_user}:{mongodb_password}@' \
                  f'{mongodb_host}:{mongodb_port}/{mongodb_db_name}?authSource={mongodb_authentication_base}'

    client = MongoClient(connect_uri)

    @rpc
    def home(self):
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
            parsed = schema.dump(data)
            schema.validate(parsed)
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

        # Pattern: client.database.collection
        product_id = self.client.products.products.insert_one(parsed).inserted_id
        self.log.info(f'products.create:: product inserted successfully id {product_id}')
        self.log.info(f'products.create:: end')
        return {'id': str(product_id)}

    @rpc
    def show(self, product_id):
        self.log.info(f'products.show:: start')
        self.log.info(f'products.show:: product id {product_id}')
        product = self.client.products.products.find_one({'_id': ObjectId(product_id)})
        product['_id'] = str(product['_id'])
        self.log.info(f'products.show:: query result {product}')
        self.log.info(f'products.show:: end')
        return product

    @rpc
    def list(self):
        self.log.info(f'products.list:: start')
        product_list = list(self.client.products.products.find())
        self.log.info(f'products.list:: query result {product_list}')
        for product in product_list:
            product['_id'] = str(product['_id'])

        self.log.info(f'products.create:: product list {product_list}')
        self.log.info(f'products.create:: end')
        return product_list


