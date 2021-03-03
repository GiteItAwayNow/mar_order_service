import uuid

from tortoise.fields import (
    CharField, DecimalField, ForeignKeyField, IntField,
    JSONField, UUIDField
)
from tortoise.models import Model

from app.core.settings import settings
from app.models.mixins import ObjChangesDatetimeMixin


class OrderProductModel(Model):
    '''Модель описывающая продукты заказа'''
    id = UUIDField(pk=True)
    product_id = UUIDField(
        description='Поле для хранения uuid продукта из сервиса каталогов'
    )
    name = CharField(max_length=28)
    description = CharField(max_length=60, null=True)
    price = DecimalField(max_digits=10, decimal_places=2)
    qty = IntField()
    image_url = CharField(max_length=255)
    catalog_id = UUIDField()
    attributes = JSONField(null=True)
    categories = JSONField()
    order = ForeignKeyField('models.OrderModel', related_name='products')

    class Meta:
        table = 'order_products'
