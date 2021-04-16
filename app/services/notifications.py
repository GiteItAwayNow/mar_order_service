import json

from kafka import KafkaProducer

from app.core.settings import settings


class NotificationSender():
    '''Сгруппировать данные оповещения в JSON
    и отправить в нужный Kafka топик

    '''
    def __init__(self):
        '''Инициализировать продюссера Кафки'''
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BROKERS
        )

    @staticmethod
    def get_object_id(obj):
        '''Получить строковое представление
        uuid объекта

        '''
        return obj['id'].__str__()

    def group_notification_data(
        self, type, data_obj, recipient_id, 
        sender=None, save_notification=False
        ):
        '''Сгруппировать данные объекта в JSON

        Args:
        -----------------------
        type: str
            тип уведомления
        data_obj: Tortoise Model obj
            объект, данные которого нужно отправить
        recipient_id: UUID
            UUID пользователя получателя уведомления
        sender: dict
            данные пользователя отправителя
        save_notification:
            флаг, показывающий нужно ли будет
            сохранить это уведомлене

        Returns:
        -----------------------
        notification_data: dict
            данные оповещения

        '''
        notification_data = {
            'type': type,
            'recipient_id': recipient_id.__str__(),
            'save_notification': save_notification
        }

        # Добавить статус заказа
        if data_obj:
            notification_data['payload'] = {
                'text': data_obj.status.value,
                'order_id': data_obj.id.__str__()
            }

        # Добавить данные пользователя отправителя
        if sender:
            notification_data['sender'] = {
                'id': self.get_object_id(sender),
                'username': sender['username'],
                'avatar_url': sender['avatar_url'],
                'profile_type': sender['profile_type']
            }

        return notification_data

    def send(self, notification_data):
        '''Отправить данные оповещения в нужный топик'''
        try:
            self.producer.send(
                settings.NOTIFICATIONS_TOPIC,
                json.dumps(notification_data).encode('utf-8')
            )
        except Exception:
            # TODO: add log
            pass


notification_sender = NotificationSender()
