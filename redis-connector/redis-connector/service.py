import json

from nameko.rpc import rpc
from nameko_redis import Redis
from nameko_structlog import StructlogDependency


class RedisConnectorService(object):
    name = 'redis-connector'
    log = StructlogDependency()
    connection = Redis('production')

    @rpc
    def health_check(self):
        self.log.info(f'redis-connector.health_check:: start')
        response = {
            'ok': True
        }
        try:
            self.connection.ping()
        except Exception as error:
            self.log.info(f'redis-connector.health_check:: ERROR Redis is not running')
            response['ok'] = False

        self.log.info(f'redis-connector.health_check:: response {response}')
        self.log.info(f'redis-connector.health_check:: end')
        return response

    @rpc
    def save(self, key, value, is_json=False):
        self.log.info(f'redis-connector.save:: start')
        self.log.info(f'redis-connector.save:: key {key}')
        self.log.info(f'redis-connector.save:: value {value}')
        self.log.info(f'redis-connector.save:: is json {is_json}')
        data = value
        if is_json:
            data = json.dumps(value)

        is_saved = self.connection.set(key, data)
        self.log.info(f'redis-connector.save:: is saved {is_saved}')
        self.log.info(f'redis-connector.save:: end')
        return is_saved

    @rpc
    def get(self, key, is_json=False):
        self.log.info(f'redis-connector.get:: start')
        self.log.info(f'redis-connector.get:: key {key}')
        self.log.info(f'redis-connector.save:: is json {is_json}')
        data = self.connection.get(key)
        self.log.info(f'redis-connector.get:: data {data}')
        if not data:
            self.log.info(f'redis-connector.get:: nothing was found with key {key}')
            self.log.info(f'redis-connector.get:: end')
            return None

        if is_json:
            data = json.loads(data)

        self.log.info(f'redis-connector.get:: returning {data}')
        self.log.info(f'redis-connector.get:: end')
        return data

    @rpc
    def delete(self, key):
        self.log.info(f'redis-connector.delete:: start')
        self.log.info(f'redis-connector.delete:: key {key}')
        result = self.connection.delete(key)
        self.log.info(f'redis-connector.delete:: result {result}')

        result = True if result == 1 else False
        self.log.info(f'redis-connector.delete:: returning {result}')
        self.log.info(f'redis-connector.delete:: end')
        return result
