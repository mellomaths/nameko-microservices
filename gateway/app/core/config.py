from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    api_version: str

    rabbit_user: str = 'guest'
    rabbit_password: str = 'guest'
    rabbit_host: str = 'localhost'
    rabbit_port: int = 5672

    @property
    def amqp_uri(self):
        return f'amqp://{self.rabbit_user}:{self.rabbit_password}@{self.rabbit_host}:{self.rabbit_port}/'

    @property
    def api_path(self):
        return f'/api/{self.api_version}'

    @property
    def cluster_rpc_proxy_config(self):
        return {
            'AMQP_URI': self.amqp_uri
        }


@lru_cache()
def get_settings():
    return Settings()
