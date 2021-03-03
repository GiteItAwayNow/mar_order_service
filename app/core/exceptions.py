from typing import Any, Dict, Optional

from fastapi import HTTPException


class ObjectDoesNotExist(HTTPException):
    '''Возбуждается, если объекта в БД не существует'''

    def __init__(self, obj_name='Object', headers: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=404,
            detail=f'{obj_name} does not exist'
        )
        self.headers = headers
