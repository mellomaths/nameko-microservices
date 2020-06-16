from nameko.rpc import RpcProxy, rpc


class HelloWorldService:
    name = 'hello_world_service'

    message_rpc = RpcProxy('message')

    @rpc
    def say_hello(self, name):
        message = self.message_rpc.hello_world()
        result = f'{message} Your name is {name}'
        return result
