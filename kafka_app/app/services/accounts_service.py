from aiohttp import ClientSession

from app.core.settings import settings


class AccountService():
    '''Сервис для получения данных из сервиса аккаунтов'''

    async def get_business_profile_data(self, business_profile_id):
        '''Получить данные нужного бизнес профиля
        из сервиса аккаунтов

        '''
        raw_business_profile_url = (
            f'{settings.ACCOUNTS_SERVICE_ADDRESS}{settings.BUSINESS_PROFILE_DATA_ENDPOINT}'
        )
        business_profile_url = raw_business_profile_url.format(business_profile_id)
        business_profile_data = await self.send_request(business_profile_url)

        return business_profile_data

    @staticmethod
    async def send_request(data_url):
        '''Отправить запрос в сервис аккаунтов,
        чтобы получить данные с нужного эндпоинта

        '''
        async with ClientSession() as session:
            async with session.get(data_url) as response:
                response_json = await response.json()

                return response_json


accounts_service = AccountService()
