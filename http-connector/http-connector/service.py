import json

from nameko.rpc import RpcProxy

from nameko_structlog import StructlogDependency

from werkzeug import Response

from .entrypoints import http


class HttpService(object):
    name = 'httpConnector'
    log = StructlogDependency()

    api_version = 'v1'
    base_url = f'/api/{api_version}'

    products_rpc = RpcProxy('products')

    @http('GET', f'{base_url}/services/health')
    def services_health(self, request):
        self.log.info(f'httpConnector.services_heath:: start')

        self.log.info(f'httpConnector.services_heath:: requesting products rpc')
        products_message = self.products_rpc.home()
        self.log.info(f'httpConnector.services_heath:: products rpc response {products_message}')

        json_data = {
            'products': products_message
        }

        data = json.dumps(json_data)
        self.log.info(f'httpConnector.services_heath:: data {data}')
        self.log.info(f'httpConnector.services_heath:: end')
        return Response(
            data,
            status=200,
            mimetype='application/json'
        )

    @http('POST', f'{base_url}/products')
    def create_product(self, request):
        self.log.info(f'httpConnector.create_products:: start')
        data = request.data
        self.log.info(f'httpConnector.create_products:: body request {data}')
        status_code = 200
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError as err:
            self.log.info(f'httpConnector.create_products:: body in request is not a valid json')
            status_code = 400
            error_response = {
                'status_code': status_code,
                'error': {
                    'code': 'INVALID_JSON',
                    'description': 'Body request should be a valid JSON.'
                }
            }
            self.log.info(f'httpConnector.create_products:: error response {error_response}')
            self.log.info(f'httpConnector.create_products:: status code {status_code}')
            self.log.info(f'httpConnector.create_products:: end')
            return Response(
                json.dumps(error_response),
                mimetype='application/json',
                status=status_code
            )

        service_response = self.products_rpc.create(json_data)
        if 'id' in service_response:
            status_code = 201
            product_id = service_response['id']
            self.log.info(f'httpConnector.create_products:: product id {product_id}')
            self.log.info(f'httpConnector.create_products:: status code {status_code}')
            self.log.info(f'httpConnector.create_products:: returning empty body')
            self.log.info(f'httpConnector.create_products:: end')
            return Response(
                '',
                status=status_code,
                mimetype='application/json',
                headers={'Location': product_id}
            )

        if 'error' in service_response:
            if service_response['error']['code'] == "VALIDATION_ERROR":
                status_code = 422
                self.log.info(f'httpConnector.create_products:: error response {service_response}')
                self.log.info(f'httpConnector.create_products:: status code {status_code}')
                self.log.info(f'httpConnector.create_products:: end')
                return Response(
                    json.dumps({'status_code': status_code, 'error': service_response['error']}),
                    status=status_code,
                    mimetype='application/json'
                )

        status_code = 500
        error_response = {
            'status_code': status_code,
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'description': 'Something not expected happened while creating a product'
            }
        }

        self.log.info(f'httpConnector.create_products:: status code {status_code}')
        self.log.info(f'httpConnector.create_products:: error response {error_response}')
        self.log.info(f'httpConnector.create_products:: end')
        return Response(
            json.dumps(error_response),
            status=status_code,
            mimetype='application/json',
        )
