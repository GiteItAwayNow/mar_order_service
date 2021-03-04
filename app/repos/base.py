from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.core.exceptions import ObjectDoesNotExist


class BaseRepo():
    '''Класс с методами CRUD операций'''

    async def bulk_create(self, objects_data):
        '''Сделать массовое создание объектов в БД

        objects_data: list[dict]
            список с данными для каждого объекта,
            который нужно создать

        '''
        objects_to_create = [
            self.db_model(**object_data) for object_data in objects_data
        ]

        await self.db_model.bulk_create(objects_to_create)

    async def create_object(self, obj_data_dict={}):
        '''Создать новый объект в БД

        Args:
        -----------------------
        obj_data_dict: dict
            данные для создания нового объекта

        Returns:
        -----------------------
        obj: Tortoise ORM Model object
            созданный объект

        '''
        try:
            obj = self.db_model(**obj_data_dict)

            await obj.save()
        except IntegrityError as exception:
            raise HTTPException(
                status_code=409, detail=f'{exception}'
            )

        return obj

    def make_get_object_queryset(self, filters={}, related_fields=[]):
        '''Создать Queryset объект, чтобы прочитать определенный объект
        из БД

        Args:
        -----------------------
        filters: dict
            фильтры, по которым надо получить
            нужный объект
        related_fields: list[str]
            список связанных объектов, которые должны быть
            запрефетчены(присоединены к запрашиваемому объекту).
            Объекты, которые связаны с нужным какой-от связью(
            one-to-one, m2m, etc.)

        Returns:
        -----------------------
        Tortoise Queryset object
            Queryset, после исполнения которого
            вернется нужный объект

        '''
        return self.db_model.get(**filters).prefetch_related(*related_fields)

    def make_get_objects_list_queryset(
        self, filters={}, related_fields=[], limit=None, offset=None, order_by=[],
        values_list=[], values_list_flat_flag=True
        ):
        '''Create queryset to get list of objects from the DB

        Args:
        -----------------------
        filters: dict
            фильтры, по которым надо получить
            нужный объект
        related_fields: list[str]
            список связанных объектов, которые должны быть
            запрефетчены(присоединены к запрашиваемому объекту).
            Объекты, которые связаны с нужным какой-от связью(
            one-to-one, m2m, etc.)
        limit: int
            лимит объектов, которое надо получить
        offset: int
            стартовая позиция(индекс) для отсчета,
            с какого элемента стоит начинать при выборке
        order_by: list[str]
            список полей для упорядочивания объектов

        Returns:
        -----------------------
        Tortoise Queryset object
            Queryset, после исполнения
            которого вернется список нужных объект

        '''
        object_list_query = self.db_model.filter(**filters).prefetch_related(
            *related_fields).order_by(*order_by
        )

        if limit:
            object_list_query = object_list_query.limit(limit)
        if offset:
            object_list_query = object_list_query.offset(offset)
        if values_list:
            object_list_query = object_list_query.values_list(
                *values_list, flat=values_list_flat_flag
            )

        return object_list_query

    async def get_object(self, filters={}, related_fields=[]):
        '''Получить нужный объект из БД

        Args:
        -----------------------
        filters: dict
            фильтры, по которым надо получить
            нужный объект
        related_fields: list[str]
            список связанных объектов, которые должны быть
            запрефетчены(присоединены к запрашиваемому объекту).
            Объекты, которые связаны с нужным какой-от связью(
            one-to-one, m2m, etc.)

        Returns:
        -----------------------
        obj: Tortoise ORM Model object
            единственный объект, соответсвующтй запросу

        '''
        try:
            obj = await self.make_get_object_queryset(filters, related_fields)
        except DoesNotExist:
            raise ObjectDoesNotExist()

        return obj

    async def get_objects(
        self, filters={}, related_fields=[],
        limit=None, offset=None, order_by=[],
        values_list=[], values_list_flat_flag=True
        ):
        '''Получить список нужных объектов

        Args:
        -----------------------
        filters: dict
            фильтры, по которым надо получить
            нужный объект
        related_fields: list[str]
            список связанных объектов, которые должны быть
            запрефетчены(присоединены к запрашиваемому объекту).
            Объекты, которые связаны с нужным какой-от связью(
            one-to-one, m2m, etc.)
        limit: int
            лимит объектов, которое надо получить
        offset: int
            стартовая позиция(индекс) для отсчета,
            с какого элемента стоит начинать при выборке
        order_by: list[str]
            список полей для упорядочивания объектов

        Returns:
        -----------------------
        obj: List[Tortoise ORM Model objects]
            список объектов, соответсвующих запросу

        '''
        objects = await self.make_get_objects_list_queryset(
            filters, related_fields, limit, offset, order_by,
            values_list, values_list_flat_flag
        )

        return objects

    async def update_object(self, obj_data_dict, filters):
        '''Обновить объект в БД

        Args:
        -----------------------
        filters: dict
            фильтры, по которым надо получить
            нужный объект
        obj_data_dict: dict
            обновленные данные объекта

        '''
        obj = await self.get_object(filters=filters)

        update_fields = obj_data_dict.keys()
        for obj_data_field, obj_data_value in obj_data_dict.items():
            setattr(obj, obj_data_field, obj_data_value)

        if update_fields:
            await obj.save(update_fields=update_fields)

        return obj
