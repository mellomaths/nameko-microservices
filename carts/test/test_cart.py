import pytest
import uuid

from nameko.dependency_providers import Config
from nameko.testing.services import worker_factory
from redis import StrictRedis

from carts.service import CartsService


@pytest.fixture
def redis_client():
    redis_uri = 'redis://localhost:6379/11'
    client = StrictRedis.from_url(redis_uri)
    return client


@pytest.fixture
def cart_service(redis_client):
    cart_service = worker_factory(CartsService, database=redis_client)
    return cart_service


@pytest.fixture
def cart_id(cart_service):
    cart_id = cart_service.create()
    return cart_id


@pytest.fixture
def product():
    """ Create a product object
    """
    return {
        'title': 'Test Product',
        'description': 'Test Product description',
        'department': 'Test Product Department',
        'price': 1115.70,
        'quantity': 10
    }


@pytest.fixture
def product_id(cart_service, product):
    """ Create a product on Products service
    """
    service_response = cart_service.products_rpc.create(product)
    return service_response['id']


@pytest.fixture
def product_to_insert(product_id):
    return {
        'product_id': product_id,
        'amount': 1
    }


def is_hex_uuid_valid(hex_uuid):
    try:
        uuid_value = uuid.UUID(hex=hex_uuid, version=4)
    except ValueError:
        return False

    return str(hex_uuid) == str(uuid_value.hex)


def test_create_cart(cart_id):

    assert is_hex_uuid_valid(cart_id)


def test_get_empty_cart_by_id(cart_service, cart_id):

    cart = cart_service.show(cart_id)

    assert cart is not None
    products = cart.get('products')
    assert products is not None
    assert len(products) == 0


def test_insert_product_into_cart(cart_service, cart_id, product_to_insert, product):
    product_id = product_to_insert.get('product_id', None)
    product_amount = product_to_insert.get('amount', None)

    cart = cart_service.insert_product(cart_id, product_to_insert)
    print(cart)

    total_price = cart.get('total_price')
    products = cart.get('products')
    assert len(products) > 0
    assert total_price == product_amount * product.get('price')

    result = list(filter((lambda product: product['id'] == product_id), products))
    assert len(result) == 1
    assert result[0].get('amount') == product_amount
