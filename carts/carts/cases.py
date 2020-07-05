import uuid

from marshmallow import ValidationError

from .schemas import ProductSchema, CartSchema

from .exceptions import CustomValidationError


class ProductDomain:

    @staticmethod
    def load_product(data):
        try:
            product = ProductSchema().load(data)
        except ValidationError as err:
            validation = CustomValidationError()
            validation.set_validation_error('Validation Error', err.messages)
            raise validation

        return product

    @staticmethod
    def validate_product(product, product_id):
        validation = CustomValidationError()
        if not product:
            error_message = f'Product {product_id} was not found.'
            validation.set_not_found_error(error_message)

        return validation


class CartDomain:

    @staticmethod
    def create_cart():
        cart_id = uuid.uuid4().hex
        schema = CartSchema()
        cart = schema.dump({'id': cart_id})
        return cart

    @staticmethod
    def clear_cart(cart, cart_id):
        validation = CartDomain.validate_cart(cart, cart_id)
        if validation.has_errors:
            raise validation

        cart['products'] = []
        cart['total_price'] = 0
        return cart

    @staticmethod
    def validate_cart(cart, cart_id):
        validation = CustomValidationError()
        if not cart:
            error_message = f'Cart {cart_id} was not found.'
            validation.set_not_found_error(error_message)

        return validation

    @staticmethod
    def validate_cart_id(cart_id):
        validation = CustomValidationError()
        try:
            uuid.UUID(hex=cart_id, version=4)
        except ValueError:
            error_message = f'Cart ID {cart_id} is not a valid UUID.'
            errors = {'id': ['Not a valid UUID.']}
            validation.set_validation_error(error_message, errors)

        return validation

    @staticmethod
    def calculate_new_cart_total_price(current_total_price, product_price, product_amount):
        new_product_price = product_price * product_amount
        total_price = current_total_price + new_product_price
        return total_price

    @staticmethod
    def get_product_from_cart(cart, product_id):
        products = cart.get('products', [])
        result = list(filter((lambda product: product['id'] == product_id), products))
        if len(result) == 0:
            return None

        return result[0]

    @staticmethod
    def add_product_to_cart(cart, payload, product):
        product_id = product['id']
        existing_product = CartDomain.get_product_from_cart(cart, product['id'])
        if existing_product is not None:
            error_message = f'Duplicate product ID. The product {product_id} already exists in the cart.'
            validation = CustomValidationError()
            validation.set_business_rule_error(error_message)
            raise validation

        current_total_price = cart['total_price']
        product_price = product['price']
        product_amount = payload['amount']
        cart['total_price'] = CartDomain.calculate_new_cart_total_price(
            current_total_price,
            product_price,
            product_amount
        )

        payload['id'] = product_id
        # Update payload product price with the information from products service
        payload['price'] = product_price

        cart['products'].append(payload)

        schema = CartSchema()
        return schema.dump(cart)

    @staticmethod
    def remove_product_from_cart(cart, product_id):
        validation = CustomValidationError()
        product = CartDomain.get_product_from_cart(cart, product_id)
        if not product:
            error_message = f'Product {product_id} is not in the cart.'
            validation.set_not_found_error(error_message)
            raise validation

        cart['products'].remove(product)
        return cart
