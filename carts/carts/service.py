import json

from nameko.rpc import rpc, RpcProxy
from nameko_structlog import StructlogDependency

from .schemas import CartSchema

from .cases import ProductDomain, CartDomain

from .exceptions import CustomValidationError


class CartsService(object):
    name = 'carts'
    log = StructlogDependency()

    products_rpc = RpcProxy('products')
    redis_connector_rpc = RpcProxy('redis-connector')

    @rpc
    def health_check(self):
        self.log.info(f'carts.health:: start')
        response = {
            'ok': True,
            'dependencies': []
        }
        self.log.info(f'carts.health:: check dependencies health')
        redis_connector_response = self.redis_connector_rpc.health_check()
        self.log.info(f'carts.health:: redis connector health check {redis_connector_response}')

        if not redis_connector_response['ok']:
            response['ok'] = False
        response['dependencies'].append({'name': 'redis-connector', 'ok': redis_connector_response['ok']})

        self.log.info(f'carts.health:: response {response}')
        self.log.info(f'carts.health:: end')
        return response

    @rpc
    def create(self):
        self.log.info(f'carts.create:: start')
        cart = CartDomain.create_cart()
        cart_id = cart['id']
        self.redis_connector_rpc.save(cart_id, cart)
        self.log.info(f'carts.create:: cart id created {cart_id}')
        self.log.info(f'carts.create:: end')
        return cart_id

    @rpc
    def show(self, cart_id):
        self.log.info(f'carts.show:: start')
        self.log.info(f'carts.show:: cart id {cart_id}')
        validation = CartDomain.validate_cart_id(cart_id)
        if validation.has_errors:
            validation_error = validation.as_dict()
            self.log.info(f'carts.show:: cart validation error {validation_error}')
            self.log.info(f'carts.show:: end')
            return {'error': validation_error}

        cart = self.redis_connector_rpc.get(cart_id)
        validation = CartDomain.validate_cart(cart, cart_id)
        if validation.has_errors:
            validation_error = validation.as_dict()
            self.log.info(f'carts.show:: cart validation error {validation_error}')
            self.log.info(f'carts.show:: end')
            return {'error': validation_error}

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

        service_response = self.show(cart_id)
        if 'error' in service_response:
            self.log.info(f'carts.insert_product:: find cart error {service_response}')
            return service_response

        cart = service_response
        self.log.info(f'carts.insert_product:: cart {cart}')
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
        self.redis_connector_rpc.save(cart_id, cart)
        self.log.info(f'carts.insert_product:: end')
        return cart_updated

    @rpc
    def update_product(self, cart_id, product_id, data):
        pass

    @rpc
    def remove_product(self, cart_id, product_id):
        self.log.info(f'carts.remove_product:: start')
        self.log.info(f'carts.remove_product:: cart id {cart_id}')
        self.log.info(f'carts.remove_product:: product id {product_id}')
        service_response = self.show(cart_id)
        if 'error' in service_response:
            return service_response

        cart = service_response
        try:
            cart = CartDomain.remove_product_from_cart(cart, product_id)
        except CustomValidationError as validation_error:
            cart_validation_error = validation_error.as_dict()
            self.log.info(f'carts.remove_product:: cart validation error {cart_validation_error}')
            self.log.info(f'carts.remove_product:: end')
            return {'error': cart_validation_error}

        self.redis_connector_rpc.save(cart_id, cart)
        self.log.info(f'carts.remove_product:: cart {cart}')
        self.log.info(f'carts.remove_product:: end')
        return cart

    @rpc
    def clear(self, cart_id):
        self.log.info(f'carts.clear:: start')
        self.log.info(f'carts.clear:: cart id {cart_id}')
        validation = CartDomain.validate_cart_id(cart_id)
        if validation.has_errors:
            validation_error = validation.as_dict()
            self.log.info(f'carts.clear:: cart validation error {validation_error}')
            self.log.info(f'carts.clear:: end')
            return {'error': validation_error}

        cart = self.redis_connector_rpc.get(cart_id)
        self.log.info(f'carts.clear:: cart {cart}')
        try:
            cart = CartDomain.clear_cart(cart, cart_id)
        except CustomValidationError as validation_error:
            cart_validation_error = validation_error.as_dict()
            self.log.info(f'carts.clear:: product validation error {cart_validation_error}')
            self.log.info(f'carts.clear:: end')
            return {'error': cart_validation_error}

        self.log.info(f'carts.clear:: cart cleared {cart}')
        self.redis_connector_rpc.save(cart_id, cart)
        self.log.info(f'carts.clear:: end')
        return cart

    @rpc
    def delete(self, cart_id):
        pass
