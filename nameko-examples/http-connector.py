import json

from nameko.rpc import RpcProxy

from nameko.web.handlers import http

from werkzeug.wrappers import Response


class HttpConnectorService:
    name = 'http_connector'
    base_url = '/api/v1'

    customers_rpc = RpcProxy('customers')

    @http('POST', f'{base_url}/customers')
    def say_hello(self, request):
        data = json.loads(request.data)
        result = self.customers_rpc.create(data)
        customer_id = result['id']
        return Response(
            json.dumps({'id': customer_id}),
            status=201,
            mimetype='application/json',
        )
