import uuid

from tortoise.fields import CharField, CharEnumField, UUIDField
from tortoise.models import Model

from app.models.enums import OrderPaymentMethodEnum


class OrderPaymentMethodModel(Model):
    '''Модель для описания сущности способа оплаты заказа'''
    id = UUIDField(pk=True, default=uuid.uuid4)
    name = CharField(max_length=50)
    type = CharEnumField(OrderPaymentMethodEnum)

    class Meta:
        table = 'order_payment_methods'
