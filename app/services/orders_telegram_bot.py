
import pytz
from telegram import Bot

from app.core.settings import settings


class OrdersTelegramBot(Bot):
    '''Класс для отправки данных заказа в чат Телеграма'''

    @staticmethod
    def convert_datetime_to_moscow_tz(datetime_obj):
        '''Изменить часовой пояс объекта
        даты-время на московский

        '''
        moscow_tz = pytz.timezone('Europe/Moscow')
        order_datetime_moscow = datetime_obj.replace(
            tzinfo=pytz.utc).astimezone(moscow_tz
        )

        return order_datetime_moscow

    def create_order_message(
        self, order_obj, business_user_data, client_user_data, order_data_dict
        ):
        '''Распарсить данные заказа для создания сообщения
        в Телегам

        Args:
        -----------------------
        order_obj: OrderModel instance
            объект заказа
        business_user_data: dict
            данные бизнеса
        order_data_dict: данные заказа, отправленные клиентом

        Returns:
        -----------------------
        order_message: str
            сообщение с данными заказа для отправки в Телеграм

        '''
        order_datetime_moscow = self.convert_datetime_to_moscow_tz(
            order_obj.created_at
        )
        order_date = order_datetime_moscow.date()
        order_time = order_datetime_moscow.time().strftime("%H:%M:%S")

        order_products_list = "\n".join([
            f'<b>{product.name}</b> - <i>{product.qty}</i>' for product in order_obj.products
        ])

        # TODO: Возможно, надо будет заменить при интеграции доставки
        delivery_address = order_data_dict['delivery']['address']

        order_price = '{:.2f}'.format(order_obj.order_price)
        delivery_price = '{:.2f}'.format(order_obj.delivery_price)
        total_price = '{:.2f}'.format(order_obj.total_price)

        order_message = (
            f'<i>Номер заказа</i>: <b>{order_obj.number}</b>\n'
            f'<i>Логин бизнеса</i>: <b>{business_user_data["username"]}</b>\n'
            f'<i>Адрес бизнеса</i>: <b>{business_user_data["location"]["address"]}</b>\n'
            f'<i>Дата заказа</i>: <b>{order_date}</b>\n'
            f'<i>Время заказа</i>: <b>{order_time} (МСК)</b>\n\n'
            f'<i>Адрес доставки</i>: <b>{delivery_address}</b>\n'
            f'<i>Имя клиента</i>: <b>{client_user_data["name"]}</b>\n'
            f'<i>Логин клиента</i>: <b>{client_user_data["username"]}</b>\n'
            f'<i>Телефон клиента</i>: <b>{client_user_data["phone"]}</b>\n\n'
            '<i>Состав заказа</i>:\n'
            f'{order_products_list}\n\n'
            f'<i>Стоимость заказа</i>: <b>{order_price} р.</b>\n'
            f'<i>Стоимость доставки</i>: <b>{delivery_price} р.</b>\n'
            f'<i>Общая стоимость</i>: <b>{total_price} р.</b>'
        )

        return order_message

    def send_order_message(
        self, order_obj, business_user_data, client_user_data, order_data_dict
        ):
        '''Отправить сообщение с данными заказа в чат Телеграма

        Args:
        -----------------------
        order_obj: OrderModel instance
            объект заказа
        business_user_data: dict
            данные бизнеса
        order_data_dict: данные заказа, отправленные клиентом

        '''
        order_message = self.create_order_message(
            order_obj, business_user_data, client_user_data, order_data_dict
        )

        self.send_message(
            chat_id=settings.ORDERS_TELEGRAM_CHAT_ID,
            text=order_message,
            parse_mode='html'
        )


orders_telegram_bot = OrdersTelegramBot(token=settings.ORDERS_TELEGRAM_BOT_TOKEN)
