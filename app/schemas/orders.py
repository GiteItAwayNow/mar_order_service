from typing import List, Optional
from uuid import UUID

from pydantic import condecimal, constr, validator
from tortoise.contrib.pydantic.base import PydanticModel

from app.models.enums import OrderStatusEnum
from app.models.orders import OrderModel
from app.schemas.mixins import ObjChangesDatetimeMixin
from app.schemas.order_payment_methods import OrderPaymentMethodSchema
from app.schemas.order_products import OrderProductSchema
from app.schemas.utils import prepare_price_for_schema


class DeliverySchema(PydanticModel):
    '''Схема для данных о доставке'''
    address: str
    intercom: Optional[str] = None
    flat: Optional[str] = None
    entrance: Optional[int] = None
    floor: Optional[int] = None
    contact_phone: str


class OrderBaseSchema(PydanticModel):
    '''Схема для сериализации/валидации
    данных каталога

    '''
    status: OrderStatusEnum = OrderStatusEnum.PLACED
    comment: Optional[constr(max_length=500)] = None
    business_profile_id: UUID

    class Config:
        orm_mode = True
        orig_model = OrderModel


class OrderCreateSchema(OrderBaseSchema):
    '''Схема для сериализации/валидации
    данных при создании нового каталога

    '''
    payment_method_id: UUID
    delivery: DeliverySchema


class OrderReadSchema(ObjChangesDatetimeMixin, OrderBaseSchema):
    '''Схема для сериализации/валидации
    данных каталога при чтении(получении респонса)

    '''
    id: UUID
    number: str
    payment_method: OrderPaymentMethodSchema
    client_id: UUID
    delivery_price: condecimal(max_digits=10, decimal_places=2)
    order_price: condecimal(max_digits=10, decimal_places=2)
    total_price: condecimal(max_digits=10, decimal_places=2)
    products: List[OrderProductSchema]

    class Config:

        @staticmethod
        def schema_extra(schema, model):
            '''Добавить примеры и форматы для цен в схему'''
            ObjChangesDatetimeMixin.Config.schema_extra(schema, model)

            properties = schema.get('properties', {})
            price_fields = (
                'delivery_price', 'order_price', 'total_price'
            )

            for price_field in price_fields:
                properties[price_field] = prepare_price_for_schema()

    @validator('number')
    def add_leading_zeros_to_number(cls, value):
        '''Добавить к номеру заказа нули в начале до
        пятизначного значения

        '''
        return value.zfill(5)

    @validator('id', 'business_profile_id', 'client_id')
    def convert_uuid_to_str(cls, uuid_obj):
        '''Конвертировать UUID строку'''
        return uuid_obj.__str__()
