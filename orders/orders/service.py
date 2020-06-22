from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher

from nameko_structlog import StructlogDependency

from nameko_sqlalchemy import DatabaseSession

from .models import DeclarativeBase, Order, Product

from .schemas import OrderSchema


class OrdersService:
    name = 'orders'
    log = StructlogDependency()
    dispatch = EventDispatcher()

    db = DatabaseSession(DeclarativeBase)

    carts_rpc = RpcProxy('carts')

    @rpc
    def create(self, cart_id):
        self.log.info(f'orders.create:: start')
        self.log.info(f'orders.create:: cart id {cart_id}')
        cart = self.carts_rpc.show(cart_id)
        order = Order(
            total_price=cart['total_price'],
            products=[
                Product(
                    serial_number=product['id'],
                    title=product['title'],
                    description=product['description'],
                    price=product['price'],
                    quantity=product['quantity']
                )
                for product in cart['products']
            ]
        )
        self.db.add(order)
        self.db.commit()
        order = OrderSchema().dump(order)
        self.log.info(f'orders.create: order {order}')

        payload = {'order': order, 'cart_id': cart_id}
        self.dispatch('order_created', payload)
        self.log.info(f'orders.create:: end')
        return order
