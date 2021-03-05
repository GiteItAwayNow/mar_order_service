import json

from aiohttp import ClientSession

from app.core.settings import settings


class OrderChatMessageSender():
    '''Класс для формирования и отправки данных заказа
    в чат клиента

    '''
    async def send(self, order_data, chat_message_sender_jwt):
        '''Отправить сообщение в чат клиента от лица бизнеса'''
        send_message_url = f'{settings.CHATS_SERVICE_ADDRESS}{settings.SEND_CHAT_MESSAGE_ENDPOINT}'
        headers = {
            'Authorization': f'Bearer {chat_message_sender_jwt}'
        }
        order_message_data = {
            'recipients': [order_data['client_id']],
            'message': {
                'attachment': {
                    'order': order_data
                }
            }
        }

        await self.send_request(
            send_message_url,
            order_message_data,
            headers
        )

    @staticmethod
    async def send_request(url, json_data, headers):
        '''Отправить запрос в сервис чатов'''
        async with ClientSession(json_serialize=json.dumps) as session:
            await session.post(url, json=json_data, headers=headers)
            await session.close()


order_chat_message_sender = OrderChatMessageSender()
