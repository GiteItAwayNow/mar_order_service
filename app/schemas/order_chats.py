from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.schemas.users import UserSchema


class OrderChatSchema(BaseModel):
    '''Схема для сериализации данных чата,
    в который были отправлены данные заказа

    '''
    id: UUID
    chat_type: str
    business_user: UserSchema
