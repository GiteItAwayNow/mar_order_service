from fastapi import HTTPException, status
from rejson import Client, Path

from app.core.settings import settings
from app.services.decimal_json_serializers import DecimalDecoder


class CartStorage():
    '''Класс для манипуляций с корзиной в Redis'''

    def __init__(self, storage_connection_pool):
        self.storage_connection_pool = storage_connection_pool

    def delete_user_cart_json(self, user_id):
        '''Удалить корзину пользователя из хранилища

        Args:
        -----------------------
        user_id: str
            id пользователя, под
            которым хранится корзина этого юзера

        '''
        redis_server = Client(connection_pool=self.storage_connection_pool)
        redis_server.jsondel(user_id)

    def get_user_cart_json(self, user_id):
        '''Получить корзину пользователя из хранилища

        Args:
        -----------------------
        user_id: str
            id пользователя, под
            которым хранится корзина этого юзера

        Returns:
        -----------------------
        user_cart_json: dict
            данные корзины юзера из хранилища

        '''
        redis_server = Client(
            connection_pool=self.storage_connection_pool,
            decoder=DecimalDecoder()
        )
        user_cart_json = redis_server.jsonget(
            user_id, Path.rootPath(), no_escape=True
        )

        if not user_cart_json:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no cart for the user'
            )

        return user_cart_json


cart_storage = CartStorage(settings.REDIS_CONNECTION_POOL)
