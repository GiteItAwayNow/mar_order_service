from uuid import UUID

from fastapi import (
    APIRouter, Depends, HTTPException, Response, status
)
from tortoise.transactions import in_transaction

from app.repos.order_products import OrderProductRepo
from app.repos.orders import OrderRepo
from app.schemas.orders import (
    OrderCreateSchema, OrderReadSchema
)
from app.services.accounts_service import accounts_service
from app.services.cart_storage import cart_storage
from app.services.catalogs_service import catalogs_service
from app.services.chats_service import chats_service
from app.services.orders_telegram_bot import orders_telegram_bot
from app.utils.jwt_encoder import jwt_encoder
from app.utils.router_dependencies import get_user_id_from_token


router = APIRouter()


@router.post('/orders', response_model=OrderReadSchema, status_code=201)
async def create_order(
    order: OrderCreateSchema, current_user_id: str = Depends(get_user_id_from_token)
    ):
    '''Создать заказ
    \f
    Args:
    -----------------------
    order: Pydantic Model
        данные заказа
    current_user_id: str
        id текущего юзера, который добавляет продукты в корзину

    Returns:
    -----------------------
    объект Response с кодом 201

    '''
    order_data_dict = order.dict()
    order_data_dict['client_id'] = current_user_id

    user_cart_storage_json = cart_storage.get_user_cart_json(current_user_id)

    reserve_products_response_status = await catalogs_service.reserve_products(
        user_cart_storage_json
    )
    if reserve_products_response_status >= 400:
        raise HTTPException(
            status_code=409,
            detail='Not enough products in the stock'
        )

    async with in_transaction():
        order_obj = await OrderRepo().create_object(
            order_data_dict, user_cart_storage_json
        )

        await OrderProductRepo().bulk_create(order_obj, user_cart_storage_json)

        await order_obj.fetch_related('products', 'payment_method')

    cart_storage.delete_user_cart_json(current_user_id)

    # Получить данные пользователя по id его БП
    business_user_data = await accounts_service.get_business_user_data(
        order_obj.business_profile_id
    )
    # Закодировать id пользователя для отправки сообщения в чат
    business_user_jwt = jwt_encoder.encode_user_id(
        business_user_data['id']
    )
    # Отправить заказ в чат клиента
    chat_response = await chats_service.send_order(
        order_obj, business_user_jwt
    )

    chat_response['business_user'] = business_user_data
    setattr(order_obj, 'chat', chat_response)

    # TODO: возможно, в будущем это надо будет убрать,
    # если данные клиента не понадобятся
    client_user_data = await accounts_service.get_user_data(
        order_obj.client_id
    )
    # Отправить данные заказа в телеграм чат
    orders_telegram_bot.send_order_message(
        order_obj, business_user_data, client_user_data,
        order_data_dict
    )

    return order_obj
