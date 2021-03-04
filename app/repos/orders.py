from decimal import Decimal

from app.models.orders import OrderModel
from app.repos.base import BaseRepo


class OrderRepo(BaseRepo):
    '''Класс, содержащий методы для работы
    с объекатами заказов из БД

    '''
    db_model = OrderModel

    async def create_object(self, order_data_dict, user_cart_storage_json):
        '''Создать новый объект заказа

        order_data_dict: dict
            данные для создания заказа
        user_cart_storage_json: dict
            данные текущей корзины

        Returns:
        -----------------------
        order_obj: OrderModel object
            созданный объект заказа

        '''
        order_data_dict['order_price'] = Decimal(user_cart_storage_json['order_price'])
        order_data_dict['delivery_price'] = Decimal(user_cart_storage_json['delivery_price'])
        order_data_dict['total_price'] = Decimal(user_cart_storage_json['total_price'])

        order_obj = await super().create_object(order_data_dict)

        return order_obj
