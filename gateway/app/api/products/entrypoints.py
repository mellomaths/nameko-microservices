from fastapi import APIRouter, Depends
from nameko.standalone.rpc import ClusterRpcProxy

from ...core import config

from .models import ProductIn

router = APIRouter()


@router.get('/health')
def health_check(settings: config.Settings = Depends(config.get_settings)):
    with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
        return rpc.products.health_check()


@router.get('/')
def get_all_products(settings: config.Settings = Depends(config.get_settings)):
    # with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
    #     rpc.products.

    return 'Responding'


@router.get('/{product_id}')
def get_product_by_id(product_id: str):
    return


@router.post('/')
def create_product(product_in: ProductIn):
    return
