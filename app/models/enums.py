from enum import Enum


class OrderPaymentMethodEnum(str, Enum):
    '''Способы оплаты заказа'''
    CASH = 'cash'
    CARD = 'card'
    APPLE_PAY = 'apple_pay'
    GOOGLE_PAY = 'google_pay'


class OrderStatusEnum(str, Enum):
    '''Статусы заказа'''
    PLACED = 'placed'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
