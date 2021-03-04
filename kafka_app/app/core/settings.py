from typing import Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    '''Класс с настройками и переменными проекта'''
    # Kafka
    KAFKA_BROKERS: str
    SEND_ORDER_CHAT_MESSAGE: str

    # Chat service
    CHATS_SERVICE_ADDRESS: str
    SEND_CHAT_MESSAGE_ENDPOINT: str

    # Accounts service
    ACCOUNTS_SERVICE_ADDRESS: str
    BUSINESS_PROFILE_DATA_ENDPOINT: str

    @validator("KAFKA_BROKERS")
    def split_brokers_list(cls, brokers_list: str):
        '''Разделить строку с брокерами, превратив в список'''
        return brokers_list.split(',')


settings = Settings()
