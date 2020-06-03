import random
import datetime

import locust

from faker import Faker


class QuickStartUser(locust.HttpUser):
    wait_time = locust.between(1, 2)
    fake = Faker()

    @locust.task
    def test_post_products(self):
        product = self._generate_product()
        res = self.client.post('/products', json=product)

        assert res.status_code == 201
        assert res.headers.get('Location') is not None
        assert res.elapsed < datetime.timedelta(seconds=1)

        product_id_url = res.headers.get('Location')
        self.product_uris.append(product_id_url)

    @locust.task
    def test_get_products(self):
        res = self.client.get('/products')

        assert res.status_code == 200
        assert res.elapsed < datetime.timedelta(seconds=1)
        assert res.headers.get('Content-Type') == 'application/json'

    @locust.task
    def test_get_product_by_id(self):
        product = self._generate_product()
        res = self.client.post('/products', json=product)

        assert res.status_code == 201
        assert res.headers.get('Location') is not None
        assert res.elapsed < datetime.timedelta(seconds=1)

        product_by_id_url = res.headers.get('Location')

        # uri = random.choice(self.product_uris)
        res = self.client.get(product_by_id_url)

        assert res.status_code == 200
        assert res.headers.get('Content-Type') == 'application/json'
        assert res.elapsed < datetime.timedelta(seconds=1)

    def _generate_product(self):
        product = {
            'title': self.fake.name(),
            'description': self.fake.text(),
            'department': self.fake.name(),
            'price': random.uniform(1, 1000),
            'quantity': random.randint(1, 20)
        }
        return product
