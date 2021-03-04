import jwt


class JWTEncoder():
    '''Класс для кодирования данных в JWT'''
    
    def encode_chat_message_sender_id(self, business_profile_data):
        '''Закодировать id пользователя, чтобы он был вшит в токен'''
        sender_id = business_profile_data['user_id']

        chat_message_sender_jwt = jwt.encode(
            {'client_data': {'user': {'id': sender_id}}},
            'order_message',
            algorithm='HS256'
        ).decode('utf-8')

        return chat_message_sender_jwt


jwt_encoder = JWTEncoder()
