
def prepare_price_for_schema():
    '''Форматировать поля с ценами для схемы(OpenAPI)'''
    price_field_schema_data = {
        'example': 666.66,
        'format': 'Decimal(10, 2)',
        'type': 'number'
    }

    return price_field_schema_data
