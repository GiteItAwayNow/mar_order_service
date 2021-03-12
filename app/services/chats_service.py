from aiohttp import ClientSession

from app.core.settings import settings
from app.schemas.orders import OrderReadSchema
from app.utils.decimal_json_serializers import DecimalEncoder


class ChatsService():
    '''Класс для работы с сервисом чатом'''

    @staticmethod
    def make_order_message_data(order_obj):
        '''Сделать сообщение чата из данных заказа

        Args:
        -----------------------
        order_obj: OrderModel instance
            объект заказа, данные о котором надо
            отправить в чат клиенту

        Returns:
        -----------------------
        encoded_order_message_data: str
            готовое для отправки через API
            сообщение с данными заказа

        '''
        order_data = OrderReadSchema.from_orm(order_obj).dict()

        order_message_data = {
            'recipients': [order_data['client_id']],
            'message': {
                'attachment': {
                    'order': order_data
                }
            }
        }
        encoded_order_message_data = DecimalEncoder().encode(order_message_data)

        return encoded_order_message_data

    async def send_order(self, order_obj, business_user_jwt):
        '''Отправить сообщение в чат клиента от лица бизнеса

        Args:
        -----------------------
        order_obj: OrderModel instance
            объект заказа, данные о котором надо
            отправить в чат клиенту
        business_user_jwt: str
            токен бизнес пользователя, от которого будет отправлено
            сообщение в чат

        Returns:
        -----------------------
        chat_response: dict
            ответ от сервиса чатов на отправку сообщения

        '''
        send_message_url = f'{settings.CHATS_SERVICE_ADDRESS}{settings.SEND_CHAT_MESSAGE_ENDPOINT}'
        headers = {
            'Authorization': f'Bearer {business_user_jwt}'
        }
        order_message_data = self.make_order_message_data(order_obj)

        chat_response = await self.send_request(
            send_message_url,
            order_message_data,
            headers
        )

        return chat_response

    @staticmethod
    async def send_request(url, data, headers):
        '''Отправить запрос в сервис чатов

        Args:
        -----------------------
        data: str
            dump json данные, которые должны быть
            отправлены на эндпоинт
        headers: dict
            хедерсы для запроса

        Returns:
        -----------------------
        response.json(): dict
            ответ от сервиса чатов

        '''
        async with ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                return await response.json()


chats_service = ChatsService()
