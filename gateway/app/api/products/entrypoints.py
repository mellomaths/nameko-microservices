from typing import List

from fastapi import APIRouter, Depends, status, Request, Response
from fastapi.responses import JSONResponse
from nameko.standalone.rpc import ClusterRpcProxy

from ...core import config

from .models import ProductIn, ProductOut

router = APIRouter()


@router.get('/health', status_code=status.HTTP_200_OK)
def health_check(settings: config.Settings = Depends(config.get_settings)):
    with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
        return rpc.products.health_check()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductIn, request: Request, settings: config.Settings = Depends(config.get_settings)):
    with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
        service_response = rpc.products.create(product_in.dict())
        if service_response.get('error', None):
            status_code = status.HTTP_400_BAD_REQUEST
            error = service_response.get('error')
            if error.get('code', '') == 'VALIDATION_ERROR':
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

            response_data = {'status_code': status_code, 'error': error}
            return JSONResponse(content=response_data, status_code=status_code)

        product_id = service_response.get('id')
        location = f'{request.url}{product_id}'
        headers = {'Location': location, 'Entity': product_id}
        return Response(status_code=status.HTTP_201_CREATED, headers=headers)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ProductOut])
def list_all_products(settings: config.Settings = Depends(config.get_settings)):
    with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
        products = rpc.products.list()
        return JSONResponse(content=products)


@router.get('/{product_id}', status_code=status.HTTP_200_OK, response_model=ProductOut)
def get_product_by_id(product_id: str, settings: config.Settings = Depends(config.get_settings)):
    with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
        product = rpc.products.show(product_id)
        if not product:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return JSONResponse(content=product, status_code=status.HTTP_200_OK)

