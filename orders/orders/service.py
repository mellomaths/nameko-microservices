from nameko.rpc import rpc, RpcProxy

from nameko_structlog import StructlogDependency

from nameko_sqlalchemy import DatabaseSession

from .models import DeclarativeBase


class OrdersService:
    name = 'orders'
    log = StructlogDependency()

    db = DatabaseSession(DeclarativeBase)

    carts_rpc = RpcProxy('carts')

    @rpc
    def create(self, cart_id):
        pass
