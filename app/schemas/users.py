from uuid import UUID

from pydantic import BaseModel, HttpUrl


class UserSchema(BaseModel):
    '''Схема для сериализации данных юзера'''
    id: UUID
    username: str
    avatar_url: HttpUrl
    profile_type: str
