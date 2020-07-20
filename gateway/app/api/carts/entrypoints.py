from fastapi import APIRouter, Depends, status, Request, Response
from fastapi.responses import JSONResponse
from nameko.standalone.rpc import ClusterRpcProxy

from ...core import config

router = APIRouter()


@router.get('/health', status_code=status.HTTP_200_OK)
def health_check(settings: config.Settings = Depends(config.get_settings)):
    with ClusterRpcProxy(settings.cluster_rpc_proxy_config) as rpc:
        health = rpc.carts.health_check()
        if health.get('ok', False):
            return Response(status_code=status.HTTP_200_OK)

        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

