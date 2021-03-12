import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_user_id_from_token(token: str = Depends(oauth2_scheme)):
    '''Получить user_id из AUTHORIZATION token'''
    try:
        jwt_claim = jwt.decode(token, algorithms='HS256', verify=False)
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            detail='Sorry, we can\'t decode your token',
            status_code=400
        )

    try:
        user_id = jwt_claim['client_data']['user']['id']
    except KeyError:
        raise HTTPException(
            detail='Sorry, you can\'t access this resource',
            status_code=401
        )

    return user_id
