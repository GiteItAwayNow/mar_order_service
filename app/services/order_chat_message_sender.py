import json

from kafka import KafkaProducer

from app.core.settings import settings
from app.schemas.orders import OrderReadSchema
from app.services.decimal_json_serializers import DecimalEncoder


class OrderChatMessageSender():
    '''Класс для создания и отправки сообщения(данных
    заказа) в нужный топик для последующей отправки
    сообщения о заказе в чат клиента

    '''
    def __init__(self):
        '''Инициализировать продюссера Кафки'''
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BROKERS
        )

    async def make_message(self, order_obj):
        '''Конвертировать объект заказа в JSON, чтобы
        отправить его через Kafka

        Args:
        -----------------------
        order_obj: OrderMode instance
            объект заказа

        Returns:
        -----------------------
        order_message: dict
            данные заказа для отправки в чат

        '''
        await order_obj.fetch_related('products', 'payment_method')

        order_message = OrderReadSchema.from_orm(order_obj).dict()

        return order_message

    def send_message(self, order_message):
        '''Отправить данные сообщения о заказе в нужный топик'''
        try:
            encoded_order_message = DecimalEncoder().encode(
                order_message
            ).encode('utf8')
            
            self.producer.send(
                settings.SEND_ORDER_CHAT_MESSAGE,
                encoded_order_message
            )
        except AttributeError:
            # TODO: add logger
            pass


order_chat_message_sender = OrderChatMessageSender()
