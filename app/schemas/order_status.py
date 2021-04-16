from tortoise.contrib.pydantic.base import PydanticModel

from app.models.enums import OrderStatusEnum

class OrderStatusSchema(PydanticModel):
    '''Схема для сериализации/валидации
    статуса заказа
    '''
    status: OrderStatusEnum


class OrderStatusReadSchema(OrderStatusSchema):
    '''Схема для сериализации/валидации
    статуса заказа при чтении(получении респонса)
    '''


class OrderStatusUpdateSchema(OrderStatusSchema):
    '''Схема для сериализации/валидации
    статуса заказа при обновлении заказа
    '''
