import uuid

from tortoise.fields import (
    CharField, CharEnumField, DecimalField,
    ForeignKeyField, IntField, UUIDField
)
from tortoise.models import Model

from app.models.enums import OrderStatusEnum
from app.models.mixins import ObjChangesDatetimeMixin


class OrderModel(Model, ObjChangesDatetimeMixin):
    '''Модель для описания структуры хранения сущностей
    заказов в БД

    '''
    id = UUIDField(pk=True, default=uuid.uuid4)
    number = IntField(generated=True, unique=True)
    status = CharEnumField(OrderStatusEnum, default=OrderStatusEnum.PLACED)
    comment = CharField(max_length=500, null=True)
    business_profile_id = UUIDField()
    client_id = UUIDField()
    delivery_price = DecimalField(max_digits=10, decimal_places=2)
    order_price = DecimalField(max_digits=10, decimal_places=2)
    total_price = DecimalField(max_digits=10, decimal_places=2)
    payment_method = ForeignKeyField('models.OrderPaymentMethodModel')

    class Meta:
        table = 'orders'
