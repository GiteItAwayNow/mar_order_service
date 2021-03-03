from app.models.order_products import OrderProductModel
from app.repos.base import BaseRepo


class OrderProductRepo(BaseRepo):
    '''Класс(репо), модержащий методы для работы с объекатами
    продуктов заказа из БД

    '''
    db_model = OrderProductModel
