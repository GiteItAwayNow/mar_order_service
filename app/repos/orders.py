from app.models.orders import OrderModel
from app.repos.base import BaseRepo


class OrderRepo(BaseRepo):
    '''Класс, содержащий методы для работы
    с объекатами заказов из БД

    '''
    db_model = OrderModel
