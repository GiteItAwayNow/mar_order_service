from app.models.order_payment_methods import OrderPaymentMethodModel
from app.repos.base import BaseRepo


class OrderPaymentMethodRepo(BaseRepo):
    '''Класс, содержащий методы для работы
    с объекатами БД способов оплаты заказа

    '''
    db_model = OrderPaymentMethodModel
