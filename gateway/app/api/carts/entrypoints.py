from fastapi import APIRouter, Depends, status, Request, Response
from fastapi.responses import JSONResponse
from nameko.standalone.rpc import ClusterRpcProxy

from .models import ProductIn, CartOut

from ..deps import map_error_code_to_status_code

from ...core import config

router = APIRouter()


@router.get('/health', status_code=status.HTTP_200_OK)
def health_check(settings: config.Settings = Depends(config.get_settings)):
    with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
        health = rpc.carts.health_check()
        if health.get('ok', False):
            return Response(status_code=status.HTTP_200_OK)

        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_cart(request: Request, settings: config.Settings = Depends(config.get_settings)):
    with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
        cart_id = rpc.carts.create()
        headers = {'Location': f'{request.url}{cart_id}', 'Entity': cart_id}
        return Response(status_code=status.HTTP_201_CREATED, headers=headers)


@router.get('/{cart_id}', status_code=status.HTTP_200_OK, response_model=CartOut)
def get_cart_by_id(cart_id: str, settings: config.Settings = Depends(config.get_settings)):
    with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
        service_response = rpc.carts.show(cart_id)
        error = service_response.get('error', None)
        if error:
            status_code = map_error_code_to_status_code(error.get('code'))
            error_response = {
                'status_code': status_code,
                'error': error
            }
            return JSONResponse(content=error_response, status_code=status_code)

        return JSONResponse(content=service_response, status_code=status.HTTP_200_OK)


@router.post('/{cart_id}/products', status_code=status.HTTP_201_CREATED)
def insert_product_into_cart(cart_id: str, product_in: ProductIn, request: Request,
                             settings: config.Settings = Depends(config.get_settings)):
    with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
        service_response = rpc.carts.insert_product(cart_id, product_in.dict())
        error = service_response.get('error', None)
        if error:
            status_code = map_error_code_to_status_code(error.get('code'))
            error_response = {
                'status_code': status_code,
                'error': error
            }
            return JSONResponse(content=error_response, status_code=status_code)

        headers = {'Location': f'{request.url}/{product_in.product_id}', 'Entity': product_in.product_id}
        return JSONResponse(content=service_response, status_code=status.HTTP_201_CREATED, headers=headers)


@router.delete('/{cart_id}/products/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_product_from_cart(cart_id: str, product_id: str, settings: config.Settings = Depends(config.get_settings)):
    with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
        service_response = rpc.carts.remove_product(cart_id, product_id)
        error = service_response.get('error', None)
        if error:
            status_code = map_error_code_to_status_code(error.get('code'))
            if status_code != status.HTTP_404_NOT_FOUND:
                error_response = {
                    'status_code': status_code,
                    'error': error
                }

                return JSONResponse(content=error_response, status_code=status_code)

        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete('/{cart_id}/products')
def clear_cart(cart_id: str, settings: config.Settings = Depends(config.get_settings)):
    with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
        service_response = rpc.carts.clear(cart_id)
        error = service_response.get('error', None)
        if error:
            status_code = map_error_code_to_status_code(error.get('code'))
            if status_code != status.HTTP_404_NOT_FOUND:
                error_response = {
                    'status_code': status_code,
                    'error': error
                }

                return JSONResponse(content=error_response, status_code=status_code)

        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete('/{cart_id}')
def delete_cart(cart_id: str, settings: config.Settings = Depends(config.get_settings)):
    with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
        service_response = rpc.carts.delete(cart_id)
        error = service_response.get('error', None)
        if error:
            status_code = map_error_code_to_status_code(error.get('code'))
            if status_code != status.HTTP_404_NOT_FOUND:
                error_response = {
                    'status_code': status_code,
                    'error': error
                }

                return JSONResponse(content=error_response, status_code=status_code)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
