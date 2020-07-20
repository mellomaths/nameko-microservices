from fastapi import APIRouter, Depends, status, Request, Response
from fastapi.responses import JSONResponse
from nameko.standalone.rpc import ClusterRpcProxy

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


@router.get('/{cart_id}', status_code=status.HTTP_200_OK)
def get_cart_by_id(cart_id: str, settings: config.Settings = Depends(config.get_settings)):
    with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
        service_response = rpc.carts.show(cart_id)
        error = service_response.get('error', None)
        if error:
            status_code = map_error_code_to_status_code(error.get('code'))
            return Response(status_code=status_code)

        return JSONResponse(content=service_response, status_code=status.HTTP_200_OK)


