import json

from nameko.rpc import RpcProxy

from nameko_structlog import StructlogDependency

from werkzeug.wrappers import Response

from .entrypoints import http

from .helpers import map_error_code_to_status_code


class HttpService(object):
    name = 'httpConnector'
    log = StructlogDependency()

    api_version = 'v1'
    base_url = f'/api/{api_version}'

    products_rpc = RpcProxy('products')
    cart_rpc = RpcProxy('carts')
    orders_rpc = RpcProxy('orders')

    @http('GET', f'{base_url}/services/health')
    def services_health(self, request):
        self.log.info(f'httpConnector.services_heath:: start')

        self.log.info(f'httpConnector.services_heath:: requesting products rpc')
        products_message = self.products_rpc.health_check()
        self.log.info(f'httpConnector.services_heath:: products rpc response {products_message}')

        self.log.info(f'httpConnector.services_heath:: requesting carts rpc')
        carts_message = self.cart_rpc.health_check()
        self.log.info(f'httpConnector.services_heath:: carts rpc response {carts_message}')

        self.log.info(f'httpConnector.services_heath:: requesting carts rpc')
        orders_message = self.orders_rpc.health_check()
        self.log.info(f'httpConnector.services_heath:: orders rpc response {orders_message}')

        json_data = {
            'products': products_message,
            'carts': carts_message,
            'orders': orders_message
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
        self.log.info(f'httpConnector.create_products:: products_rpc.create response {service_response}')
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

        if 'id' in service_response:
            status_code = 201
            product_id = service_response['id']
            self.log.info(f'httpConnector.create_products:: product id {product_id}')
            self.log.info(f'httpConnector.create_products:: status code {status_code}')
            self.log.info(f'httpConnector.create_products:: returning empty body')
            location = f'{request.url}/{product_id}'
            self.log.info(f'httpConnector.create_products:: location {location}')
            self.log.info(f'httpConnector.create_products:: end')
            # return status_code, {'Location': location}, ''
            return Response(
                '',
                status=status_code,
                mimetype='application/json',
                headers={'Location': location, 'Entity': product_id}
            )

        status_code = 500
        error_response = {
            'status_code': status_code,
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'description': 'Something not expected happened while creating a product.'
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

    @http('GET', f'{base_url}/products/<string:product_id>')
    def get_product_by_id(self, request, product_id):
        self.log.info(f'httpConnector.get_product_by_id:: start')
        self.log.info(f'httpConnector.get_product_by_id:: product id {product_id}')

        product = self.products_rpc.show(product_id)
        self.log.info(f'httpConnector.get_product_by_id:: products_rpc.show response {product}')
        if not product:
            status_code = 404
            error_response = {
                'status_code': status_code,
                'error': {
                    'code': 'NOT_FOUND',
                    'description': f'Product {product_id} was not found.'
                }
            }
            self.log.info(f'httpConnector.get_product_by_id:: error response {error_response}')
            self.log.info(f'httpConnector.get_product_by_id:: status code {status_code}')
            self.log.info(f'httpConnector.get_product_by_id:: end')
            return Response(
                json.dumps(error_response),
                mimetype='application/json',
                status=status_code
            )

        status_code = 200
        self.log.info(f'httpConnector.get_product_by_id:: status code {status_code}')
        self.log.info(f'httpConnector.get_product_by_id:: end')
        return Response(
            json.dumps(product),
            mimetype='application/json',
            status=status_code
        )

    @http('GET', f'{base_url}/products')
    def get_products(self, request):
        self.log.info(f'httpConnector.get_products:: start')
        products = self.products_rpc.list()
        self.log.info(f'httpConnector.get_product_by_id:: products_rpc.list response {products}')
        status_code = 200
        self.log.info(f'httpConnector.get_products:: status code {status_code}')
        self.log.info(f'httpConnector.get_products:: end')
        return Response(
            json.dumps(products),
            mimetype='application/json',
            status=status_code
        )

    @http('POST', f'{base_url}/carts')
    def create_cart(self, request):
        self.log.info(f'httpConnector.create_cart:: start')
        cart_id = self.cart_rpc.create()
        self.log.info(f'httpConnector.create_cart:: cart id created {cart_id}')
        location = f'{request.url}/{cart_id}'
        self.log.info(f'httpConnector.create_cart:: end')
        return Response(
            '',
            mimetype='application/json',
            status=201,
            headers={'Location': location, 'Entity': cart_id}
        )

    @http('GET', f'{base_url}/carts/<string:cart_id>')
    def get_cart_by_id(self, request, cart_id):
        self.log.info(f'httpConnector.get_cart_by_id:: start')
        self.log.info(f'httpConnector.get_cart_by_id:: cart id {cart_id}')
        service_response = self.cart_rpc.show(cart_id)
        self.log.info(f'httpConnector.get_cart_by_id:: cart service response {service_response}')
        if 'error' in service_response:
            status_code = map_error_code_to_status_code(service_response['error']['code'])
            error_response = {
                'status_code': status_code,
                'error': service_response['error']
            }
            self.log.info(f'httpConnector.get_cart_by_id:: error response {error_response}')
            self.log.info(f'httpConnector.get_cart_by_id:: status code {status_code}')
            self.log.info(f'httpConnector.get_cart_by_id:: end')
            return Response(
                json.dumps(error_response),
                mimetype='application/json',
                status=status_code
            )

        cart = service_response
        self.log.info(f'httpConnector.get_cart_by_id:: end')
        return Response(
            json.dumps(cart),
            mimetype='application/json',
            status=200
        )

    @http('POST', f'{base_url}/carts/<string:cart_id>/products')
    def insert_product_into_cart(self, request, cart_id):
        self.log.info(f'httpConnector.insert_product_into_cart:: start')
        self.log.info(f'httpConnector.insert_product_into_cart:: cart_id {cart_id}')
        data = request.data
        self.log.info(f'httpConnector.insert_product_into_cart:: body request {data}')
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError as err:
            self.log.info(f'httpConnector.insert_product_into_cart:: body in request is not a valid json')
            status_code = 400
            error_response = {
                'status_code': status_code,
                'error': {
                    'code': 'INVALID_JSON',
                    'description': 'Body request should be a valid JSON.'
                }
            }
            self.log.info(f'httpConnector.insert_product_into_cart:: error response {error_response}')
            self.log.info(f'httpConnector.insert_product_into_cart:: status code {status_code}')
            self.log.info(f'httpConnector.insert_product_into_cart:: end')
            return Response(
                json.dumps(error_response),
                mimetype='application/json',
                status=status_code
            )

        service_response = self.cart_rpc.insert_product(cart_id, json_data)
        self.log.info(f'httpConnector.insert_product_into_cart:: service response {service_response}')
        if 'error' in service_response:
            status_code = map_error_code_to_status_code(service_response['error']['code'])
            error_response = {
                'status_code': status_code,
                'error': service_response['error']
            }
            self.log.info(f'httpConnector.insert_product_into_cart:: error response {error_response}')
            self.log.info(f'httpConnector.insert_product_into_cart:: status code {status_code}')
            self.log.info(f'httpConnector.insert_product_into_cart:: end')
            return Response(
                json.dumps(error_response),
                mimetype='application/json',
                status=status_code
            )

        cart = service_response
        product_id = json_data['product_id']
        location = f'{request.url}/{product_id}'
        self.log.info(f'httpConnector.insert_product_into_cart:: end')
        return Response(
            json.dumps(cart),
            mimetype='application/json',
            status=201,
            headers={'Location': location}
        )

    @http('PUT', f'{base_url}/carts/<string:cart_id>/products/<string:product_id>')
    def update_product_info_in_cart(self, request, cart_id, product_id):
        pass

    @http('DELETE', f'{base_url}/carts/<string:cart_id>/products/<string:product_id>')
    def remove_product_from_cart(self, request, cart_id, product_id):
        self.log.info(f'httpConnector.remove_product_from_cart:: start')
        self.log.info(f'httpConnector.remove_product_from_cart:: cart id {cart_id}')
        self.log.info(f'httpConnector.remove_product_from_cart:: product id {product_id}')
        service_response = self.cart_rpc.remove_product(cart_id, product_id)
        # self.log.info(f'httpConnector.remove_product_from_cart:: service response {service_response}')
        if 'error' in service_response:
            service_response_error = service_response['error']
            self.log.info(f'httpConnector.remove_product_from_cart:: service response error {service_response_error}')

        self.log.info(f'httpConnector.remove_product_from_cart:: end')
        return Response(
            '',
            status=204
        )

    @http('DELETE', f'{base_url}/carts/<string:cart_id>/products')
    def clear_cart(self, request, cart_id):
        self.log.info(f'httpConnector.delete_cart:: start')
        self.log.info(f'httpConnector.delete_cart:: cart id {cart_id}')

        service_response = self.cart_rpc.clear(cart_id)
        if 'error' in service_response:
            service_response_error = service_response['error']
            self.log.info(f'httpConnector.insert_product_into_cart:: service response error {service_response_error}')

        self.log.info(f'httpConnector.delete_cart:: end')
        return Response(
            '',
            status=204
        )

    @http('DELETE', f'{base_url}/carts/<string:cart_id>')
    def delete_cart(self, request, cart_id):
        pass

    @http('POST', f'{base_url}/orders')
    def create_order(self, request):
        self.log.info(f'httpConnector.create_order:: start')
        cart_id = request.args.get('cartId', None)
        self.log.info(f'httpConnector.create_order:: cart_id {cart_id}')
        if not cart_id:
            status_code = 400
            error_response = {
                'status_code': status_code,
                'error': {
                    'code': 'INVALID_REQUEST',
                    'description': f'Query param cartId is required.'
                }
            }
            self.log.info(f'httpConnector.create_order:: error response {error_response}')
            self.log.info(f'httpConnector.create_order:: status code {status_code}')
            self.log.info(f'httpConnector.create_order:: end')
            return Response(
                json.dumps(error_response),
                mimetype='application/json',
                status=status_code
            )

        order = self.orders_rpc.create(cart_id)
        order_id = order['id']
        self.log.info(f'httpConnector.create_order:: order id created {order_id}')
        location = f'{request.url}/{order_id}'
        self.log.info(f'httpConnector.create_order:: end')
        return Response(
            '',
            mimetype='application/json',
            status=201,
            headers={'Location': location}
        )
