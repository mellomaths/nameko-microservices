from nameko.rpc import RpcProxy, rpc
from nameko.events import EventDispatcher


class CustomersService:
    name = 'customers'

    database_connector = RpcProxy('database_connector')
    dispatch = EventDispatcher()

    @rpc
    def create(self, data):
        print('Received data')
        print(data)
        customer_id = self.database_connector.save_customer(data)
        print('Customer created.')
        print('ID: ')
        print(customer_id)

        email = data['email']
        phone = data['phone']
        name = data['name']
        payload = {'email': email, 'phone': phone, 'name': name, 'id': customer_id}
        self.dispatch('customer_created', payload)
        return {'id': customer_id}
