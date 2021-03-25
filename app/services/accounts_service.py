from aiohttp import ClientSession

from app.core.settings import settings


class AccountsService():
    '''Сервис для получения данных из сервиса аккаунтов'''

    async def get_business_user_data(self, business_profile_id):
        '''Получить данные пользователя из сервиса аккаунтов
        по id его бизнес-профиля

        Args:
        -----------------------
        business_profile_id: UUID
            id бизнес-профиля пользователя

        Returns:
        -----------------------
        business_user_data: dict
            данными пользователя-бизнеса

        '''
        raw_business_user_url = (
            f'{settings.ACCOUNTS_SERVICE_ADDRESS}{settings.GET_USER_BY_BUSINESS_ID_ENDPOINT}'
        )
        business_user_url = raw_business_user_url.format(business_profile_id)
        business_user_data = await self.send_request(business_user_url)

        return business_user_data

    async def get_user_data(self, user_id):
        '''Получить данные пользователя из сервиса аккаунтов
        по его id

        Args:
        -----------------------
        user_id: UUID
            id пользователя

        Returns:
        -----------------------
        user_data: dict
            данными пользователя

        '''
        # TODO: Если получение данных клиента(заказчика)
        # останется, то надо будет вынести эндпоинт в переменную
        # окружения
        user_url = (
            f'{settings.ACCOUNTS_SERVICE_ADDRESS}/v1/users/{user_id}'
        )
        user_data = await self.send_request(user_url)

        return user_data

    @staticmethod
    async def send_request(data_url):
        '''Отправить запрос в сервис аккаунтов,
        чтобы получить данные с нужного эндпоинта

        Args:
        -----------------------
        data_url: str
            адрес, на который надо отправить запрос

        Returns:
        -----------------------
        response_json: dict
            JSON ответ от эндпоинта

        '''
        async with ClientSession() as session:
            async with session.get(data_url) as response:
                response_json = await response.json()

                return response_json


accounts_service = AccountsService()
