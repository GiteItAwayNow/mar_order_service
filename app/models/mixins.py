from tortoise.fields import DatetimeField


class ObjChangesDatetimeMixin():
    '''Mixin containing datetime fields to describe changes
    in an object

    '''
    created_at = DatetimeField(null=False, auto_now_add=True)
    updated_at = DatetimeField(null=False, auto_now=True)
    deleted_at = DatetimeField(null=True)
