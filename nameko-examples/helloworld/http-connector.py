from nameko.rpc import RpcProxy

from nameko.web.handlers import http


class HttpConnectorService:
    name = 'http_connector'
    base_url = '/api/v1'

    hello_world_rpc = RpcProxy('hello_world_service')

    @http('GET', f'{base_url}/hello/<string:name>')
    def say_hello(self, request, name):
        message = self.hello_world_rpc.say_hello(name)
        return message
