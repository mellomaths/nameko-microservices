import uuid
import json

from nameko.rpc import rpc, RpcProxy
from nameko_redis import Redis
from nameko_structlog import StructlogDependency

from marshmallow import ValidationError

from .schemas import CartSchema, ProductSchema


class CartsService(object):
    name = 'carts'
    log = StructlogDependency()

    database = Redis('production')

    products_rpc = RpcProxy('products')

    def _set_json(self, key, json_data):
        self.database.set(key, json.dumps(json_data))
        return key

    def _get_json(self, key):
        data = self.database.get(key)
        if not data:
            return None
        return json.loads(data)

    @rpc
    def create(self):
        self.log.info(f'carts.create:: start')
        cart_id = uuid.uuid4().hex
        schema = CartSchema()
        cart = schema.dump({'id': cart_id})
        self._set_json(cart_id, cart)
        self.log.info(f'carts.create:: cart id created {cart_id}')
        self.log.info(f'carts.create:: end')
        return cart_id

    @rpc
    def show(self, cart_id):
        self.log.info(f'carts.show:: start')
        self.log.info(f'carts.show:: cart id {cart_id}')
        cart = self._get_json(cart_id)
        self.log.info(f'carts.show:: cart {cart}')
        self.log.info(f'carts.show:: end')
        return cart

    @rpc
    def insert_product(self, cart_id, data):
        self.log.info(f'carts.insert_product:: start')
        self.log.info(f'carts.insert_product:: cart id {cart_id}')
        self.log.info(f'carts.insert_product:: data received {data}')
        try:
            product_info = ProductSchema().load(data)
        except ValidationError as err:
            self.log.info(f'carts.insert_product:: validation error {err}')
            error_response = {
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'description': 'Validation Error',
                    'validations': err.messages
                }
            }
            return error_response

        cart = self.show(cart_id)
        self.log.info(f'carts.insert_product:: cart {cart}')
        if not cart:
            self.log.info(f'carts.insert_product:: cart not found')
            error_response = {
                'error': {
                    'code': 'NOT_FOUND',
                    'description': f'Cart {cart_id} was not found.'
                }
            }
            self.log.info(f'carts.insert_product:: error response {error_response}')
            self.log.info(f'carts.insert_product:: end')
            return error_response

        product_id = product_info['product_id']
        product = self.products_rpc.show(product_id)
        self.log.info(f'carts.insert_product:: product {product}')
        if not product:
            self.log.info(f'carts.insert_product:: product not found')
            error_response = {
                'error': {
                    'code': 'NOT_FOUND',
                    'description': f'Product {product_id} was not found.'
                }
            }
            self.log.info(f'carts.insert_product:: error response {error_response}')
            self.log.info(f'carts.insert_product:: end')
            return error_response

        cart['total_price'] += product['price'] * product_info['amount']
        product_info['price'] = product['price']
        self.log.info(f'carts.insert_product:: product added to cart {product_info}')
        cart['products'].append(product_info)
        self._set_json(cart_id, cart)
        self.log.info(f'carts.insert_product:: end')
        return cart

    @rpc
    def update_product(self, cart_id, product_id, data):
        pass

    @rpc
    def remove_product(self, cart_id, product_id):
        pass

    @rpc
    def clear(self, cart_id):
        cart = self._get_json(cart_id)
        if not cart:
            return None

        cart['products'] = []
        cart['total_price'] = 0
        self._set_json(cart_id, cart)
        return cart

    @rpc
    def delete(self, cart_id):
        pass
