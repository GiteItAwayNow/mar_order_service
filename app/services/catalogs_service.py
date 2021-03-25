from aiohttp import ClientSession

from app.core.settings import settings


class CatalogsService():
    '''Сервис для обновления данных в сервисе каталогов'''
    update_stock_url = (
        f'{settings.CATALOGS_SERVICE_ADDRESS}{settings.UPDATE_STOCK_ENDPOINT}'
    )

    async def reserve_products(self, user_cart_storage_json):
        '''Отправить запрос на сервис каталогов, чтобы
        зарезервировать нужное количество продуктов в стоке

        Args:
        -----------------------
        user_cart_storage_json: dict
            корзина пользователя, содержащая
            продукты

        '''
        order_products_qty_data = [
            {'id': product['id'], 'qty': -product['cart_qty']}
            for product in user_cart_storage_json['products']
        ]

        reserve_products_response_status = await self.send_request(
            self.update_stock_url, order_products_qty_data
        )

        return reserve_products_response_status

    @staticmethod
    async def send_request(data_url, data):
        '''Отправить PATCH запрос в сервис каталогов,
        чтобы получить обновить данные

        Args:
        -----------------------
        data_url: str
            адрес, на который надо отправить запрос
        data: dict
            данные, отправляемые в запросе

        Returns:
        -----------------------
        response_json: dict
            JSON ответ от эндпоинта

        '''
        async with ClientSession() as session:
            async with session.patch(data_url, json=data) as response:
                response_status = response.status

                return response_status


catalogs_service = CatalogsService()
