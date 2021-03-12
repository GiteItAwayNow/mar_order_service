from decimal import Decimal
from json import JSONDecoder, JSONEncoder

import simplejson


class DecimalEncoder(JSONEncoder):
    '''Кастомный энкодер с типом Decimal'''

    def default(self, obj):
        '''Кодировать Decimal в строку для сериализации в JSON'''
        if isinstance(obj, Decimal):
            return simplejson.dumps(obj, use_decimal=True)

        return JSONEncoder.encode(self, obj)


class DecimalDecoder(JSONDecoder):
    '''Класс для кодирования типа Decimal в строку'''
    price_fields = (
        'delivery_price', 'to_free_delivery', 'order_price', 'total_price'
    )

    def decode(self, obj):
        '''Декодировать строки с ценами в Decimal'''
        storage_cart_json = JSONDecoder.decode(self, obj)

        for product in storage_cart_json['products']:
            product['price'] = simplejson.loads(product['price'], use_decimal=True)

        for price_field in self.price_fields:
            storage_cart_json[price_field] = simplejson.loads(
                storage_cart_json[price_field], use_decimal=True
            )

        return storage_cart_json
