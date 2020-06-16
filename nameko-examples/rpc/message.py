from nameko.rpc import rpc


class MessageService:
    name = 'message'

    @rpc
    def hello_world(self):
        return 'Hello World!'
