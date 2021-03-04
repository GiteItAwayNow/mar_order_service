from app.models.order_products import OrderProductModel
from app.repos.base import BaseRepo


class OrderProductRepo(BaseRepo):
    '''Класс(репо), модержащий методы для работы с объекатами
    продуктов заказа из БД

    '''
    db_model = OrderProductModel

    async def bulk_create(self, order_obj, user_cart_storage_json):
        '''Создать сразу все продукты из заказа(сохранить их в БД)

        order_obj: OrderModel instance
            объект, созданного заказа
        user_cart_storage_json: dict
            данные текущей корзины

        '''
        products = user_cart_storage_json['products']

        for product in products:
            product['product_id'] = product.pop('id')
            product['qty'] = product.pop('cart_qty')
            product['order_id'] = order_obj.id
            # TODO: мок, добавить актуальные категории
            product['categories'] = [{
                'id': '704f5f67-93f9-405d-a51b-df63c2821bc1',
                'name': 'Это просто мок'
            }]

        await super().bulk_create(products)
