from nameko.rpc import RpcProxy, rpc


class CustomersService:
    name = 'customers'

    database_connector = RpcProxy('database_connector')

    @rpc
    def create(self, data):
        print('Received data')
        print(data)
        customer_id = self.database_connector.save_customer(data)
        print('Customer created.')
        print('ID: ')
        print(customer_id)
        return {'id': customer_id}
