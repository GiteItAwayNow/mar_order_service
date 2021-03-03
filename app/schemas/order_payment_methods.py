from uuid import UUID

from pydantic import constr, validator
from tortoise.contrib.pydantic.base import PydanticModel

from app.models.enums import OrderPaymentMethodEnum
from app.models.order_payment_methods import OrderPaymentMethodModel


class OrderPaymentMethodSchema(PydanticModel):
    '''Схема для сериализации/валидации
    данных способов оплаты заказа

    '''
    id: UUID
    name: constr(max_length=50)
    type: OrderPaymentMethodEnum

    class Config:
        orm_mode = True
        orig_model = OrderPaymentMethodModel

    @validator('id')
    def convert_uuid_to_str(cls, uuid_obj):
        '''Конвертировать UUID строку'''
        return uuid_obj.__str__()
