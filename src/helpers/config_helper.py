import os
import logging
from typing import Literal, Optional, Union
from functools import lru_cache

from pydantic import BaseSettings, HttpUrl, SecretStr, validator, StrictInt
from dotenv import dotenv_values

class Settings(BaseSettings):
    environment: Literal['local', 'production']
    host: str
    port: StrictInt
    api_base_url: HttpUrl
    api_secret: SecretStr
    debug: bool = False
    auto_reload: bool = False
    sentry_integration: bool = False
    sentry_env: Optional[Literal['development', 'production']]
    sentry_dsn: Optional[HttpUrl]

    @validator('*', pre=True)
    def convert_string_to_bool(cls, v):
        if v in ['True', 'False']:
            return True if v == 'True' else False
        return v

    @validator('port', pre=True)
    def convert_port_to_integer(cls, v):
        try:
            v = int(v)
            if 64000 >= v >= 1:
                return v
            raise Exception(f'Port must be between the range(1, 64000). Yours is {v}')
        except ValueError:
            raise Exception(f'Port must be an integer. Yours is {v}')


@lru_cache
def get_settings(
        environment: Literal['local', 'production', 'testing']
    ) -> BaseSettings:
    config = {
        **dotenv_values('./configs/.env'),
        **dotenv_values(f'./configs/{environment}.env')
    }
    logging.info(f"Config: <{environment}>")
    return Settings(**config)

APP_CONFIG = get_settings(os.getenv('ENVIRONMENT', 'local'))
