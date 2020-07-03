import json

from nameko.rpc import rpc, RpcProxy

from nameko_redis import Redis
from nameko_structlog import StructlogDependency

from .schemas import CartSchema

from .cases import ProductDomain, CartDomain

from .dto import CustomValidationError


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
        cart = CartDomain.create_cart()
        cart_id = cart['id']
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
            product_payload = ProductDomain.load_product(data)
        except CustomValidationError as validation_error:
            product_validation_error = validation_error.as_dict()
            self.log.info(f'carts.insert_product:: product validation error {product_validation_error}')
            self.log.info(f'carts.insert_product:: end')
            return {'error': product_validation_error}

        cart = self.show(cart_id)
        self.log.info(f'carts.insert_product:: cart {cart}')
        cart_validation = CartDomain.validate_cart(cart, cart_id)
        if cart_validation.has_errors:
            cart_validation_error = cart_validation.as_dict()
            self.log.info(f'carts.insert_product:: cart validation error {cart_validation_error}')
            self.log.info(f'carts.insert_product:: end')
            return {'error': cart_validation_error}

        product_id = product_payload['product_id']
        product = self.products_rpc.show(product_id)
        self.log.info(f'carts.insert_product:: product {product}')
        product_validation = ProductDomain.validate_product(product, product_id)
        if product_validation.has_errors:
            product_validation_error = product_validation.as_dict()
            self.log.info(f'carts.insert_product:: product validation error {product_validation_error}')
            self.log.info(f'carts.insert_product:: end')
            return {'error': product_validation_error}

        try:
            cart_updated = CartDomain.add_product_to_cart(cart, product_payload, product)
        except CustomValidationError as validation_error:
            cart_validation_error = validation_error.as_dict()
            self.log.info(f'carts.insert_product:: cart validation error {cart_validation_error}')
            self.log.info(f'carts.insert_product:: end')
            return {'error': cart_validation_error}

        self.log.info(f'carts.insert_product:: cart updated info {cart_updated}')
        self._set_json(cart_id, cart)
        self.log.info(f'carts.insert_product:: end')
        return cart_updated

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
