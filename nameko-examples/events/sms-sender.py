from nameko.events import event_handler


class SmsService:
    name = 'sms_sender'

    @event_handler('customers', 'customer_created')
    def handle_customer_creation(self, payload):
        phone = payload['phone']
        name = payload['name']
        print(f'SMS sent to name ({phone})')
        return
