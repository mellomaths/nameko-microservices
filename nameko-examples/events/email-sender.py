from nameko.events import event_handler


class EmailService:
    name = 'email_sender'

    @event_handler('customers', 'customer_created')
    def handle_customer_creation(self, payload):
        email = payload['email']
        name = payload['name']
        print(f'Email sent to {name} ({email})')
        return
