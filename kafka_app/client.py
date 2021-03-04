import asyncio
import json

from kafka import KafkaConsumer

from app.core.settings import settings
from app.services.accounts_service import accounts_service
from app.services.jwt_encoder import jwt_encoder


class KafkaClient():
    '''Класс для мониторинга, обработки и отправки
    сообщений в чат с данными заказа

    '''
    def __init__(self):
        '''Инициализировать экземпляр consumer'''
        self.consumer = KafkaConsumer(
            settings.SEND_ORDER_CHAT_MESSAGE,
            bootstrap_servers=settings.KAFKA_BROKERS,
            consumer_timeout_ms=100
        )

    async def start(self):
        '''Стартовать loop для получения новых сообщений из топика'''
        while True:
            topic_message = self.consumer.poll(timeout_ms=100, max_records=1)
            if not topic_message:
                continue

            try:
                topic_message_value = self.parse_topic_message(topic_message)
            except Exception:
                # TODO: add logger
                continue

            try:
                business_profile_id = topic_message_value['business_profile_id']
                business_profile_data = await accounts_service.get_business_profile_data(
                    business_profile_id
                )
            except Exception:
                # TODO: уточнить исключения и добавит логгер
                continue

            try:
                chat_message_sender_jwt = jwt_encoder.encode_chat_message_sender_id(
                    business_profile_data
                )
            except Exception:
                # TODO: уточнить исключения и добавит логгер
                continue


    @staticmethod
    def parse_topic_message(topic_message):
        '''Распарсить сообщение от продюссера и
        вернуть его value

        '''
        topic_message_data = list(topic_message.values())[0][0]

        topic_message_value = json.loads(
            topic_message_data.value.decode('utf-8')
        )

        return topic_message_value


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    asyncio.ensure_future(KafkaClient().start())
    loop.run_forever()
