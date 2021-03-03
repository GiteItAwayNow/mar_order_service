from typing import List, Optional
from uuid import UUID

from pydantic import condecimal, constr, HttpUrl, validator
from tortoise.contrib.pydantic.base import PydanticModel

from app.models.order_products import OrderProductModel
from app.schemas.utils import prepare_price_for_schema


class ProductAttributeSchema(PydanticModel):
    '''Схема для сериализации/валидации
    данных аттрибута продуктов

    '''
    name: str
    value: float
    unit: str


class ProductCategorySchema(PydanticModel):
    '''Схема для сериализации/валидации
    данных категории продукта

    '''
    id: UUID
    name: str

    @validator('id')
    def convert_uuid_to_str(cls, uuid_obj):
        '''Конвертировать UUID строку'''
        return uuid_obj.__str__()


class OrderProductSchema(PydanticModel):
    '''Схема для сериализации/валидации
    данных продукта из заказа

    '''
    id: UUID
    product_id: UUID
    name: str
    qty: int
    description: Optional[constr(max_length=60)] = None
    price: condecimal(max_digits=10, decimal_places=2)
    qty: int
    image_url: HttpUrl
    attributes: Optional[ProductAttributeSchema] = None
    catalog_id: UUID
    categories: List[ProductCategorySchema]

    class Config:

        orm_mode = True
        orig_model = OrderProductModel

        @staticmethod
        def schema_extra(schema, model):
            '''Добавить примеры для цены в схему'''
            properties = schema.get('properties', {})
            properties['price'] = prepare_price_for_schema()

    @validator('id', 'product_id', 'catalog_id')
    def convert_uuid_to_str(cls, uuid_obj):
        '''Конвертировать UUID строку'''
        return uuid_obj.__str__()
