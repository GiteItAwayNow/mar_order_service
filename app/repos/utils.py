
from tortoise import timezone


def add_not_deleted_filter(func):
    '''Изменить запрос в БД, добавив в
    фильтры запроса "deleted_at is null"
    
    '''
    def wrapper(self, *args, **kwargs):
        try:
            kwargs['filters']['deleted_at'] = None
        except KeyError:
            kwargs['filters'] = {'deleted_at': None}

        output = func(self, *args, **kwargs)

        return output

    return wrapper


def add_updated_at_time(func):
    '''Добавить поле updataed_at для того чтобы
    изменить время изменения объекта
    
    '''
    def wrapper(self, *args, **kwargs):
        '''Изменить updated_at поле если были
        предоставленны любые данные для изменения объекта
        
        '''
        data_to_update = args[0]

        if data_to_update:
            data_to_update['updated_at'] = timezone.now()

        output = func(self, *args, **kwargs)

        return output

    return wrapper
