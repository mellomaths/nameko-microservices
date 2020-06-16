import uuid

from nameko.rpc import rpc


class DatabaseConnectorService:
    name = 'database_connector'

    @rpc
    def save_customer(self, customer):
        print('Customer saved!')
        customer_id = uuid.uuid4()
        print('ID: ')
        print(customer_id)
        return customer_id
