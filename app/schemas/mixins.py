from datetime import datetime

from pydantic import validator
from tortoise.contrib.pydantic.base import PydanticModel


class ObjChangesDatetimeMixin(PydanticModel):
    '''Миксин, добавляющий даты создания и обновления'''
    created_at: datetime
    updated_at: datetime

    @validator('created_at', 'updated_at')
    def format_datetime(cls, datetime_obj: datetime):
        '''Отформатировать дату'''
        return datetime_obj.strftime("%Y-%m-%dT%H:%M:%S")

    class Config:

        @staticmethod
        def schema_extra(schema, model):
            '''Добавить примеры для дат в схему'''
            properties = schema.get('properties', {})
            try:
                properties['created_at']['example'] = '2021-02-31T06-06-06'
                properties['updated_at']['example'] = '2021-02-31T06-06-06'
            except KeyError:
                pass
