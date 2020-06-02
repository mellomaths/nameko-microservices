import uuid
import json

from nameko.rpc import rpc
from nameko_redis import Redis
from nameko_structlog import StructlogDependency


class CartsService(object):
    name = 'carts'
    log = StructlogDependency()

    database = Redis('production')

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
        cart_id = uuid.uuid4().hex
        cart = {'id': cart_id, 'products': []}
        self._set_json(cart_id, cart)
        return cart_id

    @rpc
    def show(self, cart_id):
        cart = self._get_json(cart_id)
        return cart

    @rpc
    def insert_product(self, cart_id, data):
        # cart.append(product)
        pass

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
        self._set_json(cart_id, cart)
        return cart

    @rpc
    def delete(self, cart_id):
        pass
