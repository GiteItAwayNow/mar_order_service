import jwt


class JWTEncoder():
    '''Класс для кодирования данных в JWT'''

    def encode_user_id(self, user_id):
        '''Закодировать id пользователя, чтобы он был вшит в токен

        Args:
        -----------------------
        user_id: UUID
            id пользователя, который будет зашит в токен

        Returns:
        -----------------------
        user_jwt: str
            JWT, содержащий id юзера

        '''
        user_jwt = jwt.encode(
            {'client_data': {'user': {'id': user_id}}},
            'order_message',
            algorithm='HS256'
        ).decode('utf-8')

        return user_jwt


jwt_encoder = JWTEncoder()
