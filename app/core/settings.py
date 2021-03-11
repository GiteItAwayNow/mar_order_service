import secrets
from typing import List, Optional

import redis
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    '''Класс с настройками и переменными проекта'''
    PROJECT_NAME: str = 'Orders Service'
    API_V1_STR: str = '/v1'
    OPENAPI_URL: str = '/orders-openapi.json'
    PROJECT_SERVERS: list = [
        {'url': 'https://market-dev.bsl.dev/api', 'description': 'Dev Server'},
        {'url': 'https://market-stage.bsl.dev/api', 'description': 'Stage Server'},
        {'url': 'https://app.perimetr.app/api', 'description': 'Prod Server'}
    ]
    IS_LOCAL: bool
    LOCAL_ROOT_PATH: str
    SERVER_ROOT_PATH: str

    # DB variables
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DATABASE_URL: Optional[PostgresDsn] = None

    # REDIS confings
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB_NUMBER: int
    REDIS_CONNECTION_POOL: Optional[redis.ConnectionPool] = None

    @validator('DATABASE_URL', pre=True)
    def assemble_db_connection(cls, value, values):
        '''Сделать урл для подключения к БД'''
        if isinstance(value, str):
            return value

        return PostgresDsn.build(
            scheme='postgres',
            user=values.get('DB_USER'),
            password=values.get('DB_PASSWORD'),
            host=values.get('DB_HOST'),
            port=values.get('DB_PORT'),
            path=f'/{values.get("DB_NAME") or ""}',
        )

    @validator('REDIS_CONNECTION_POOL', pre=True, always=True)
    def make_redis_connection_pool(cls, value, values):
        '''Создать пул подключения для Redis'''
        return redis.ConnectionPool(
            host=values.get('REDIS_HOST'),
            port=values.get('REDIS_PORT'),
            password=values.get('REDIS_PASSWORD'),
            db=values.get('REDIS_DB_NUMBER'),
            encoding='utf8',
            decode_responses=True
        )


settings = Settings()
