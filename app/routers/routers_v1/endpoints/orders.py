from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from tortoise.transactions import in_transaction

from app.repos.order_products import OrderProductRepo
from app.repos.orders import OrderRepo
from app.schemas.orders import OrderCreateSchema
from app.services.cart_storage import cart_storage
from app.services.order_chat_message_sender import order_chat_message_sender
from app.services.router_dependencies import get_user_id_from_token


router = APIRouter()


@router.post('/orders', status_code=201)
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

    async with in_transaction():
        order_obj = await OrderRepo().create_object(
            order_data_dict, user_cart_storage_json
        )

        await OrderProductRepo().bulk_create(order_obj, user_cart_storage_json)

    cart_storage.delete_user_cart_json(current_user_id)

    order_chat_message = await order_chat_message_sender.make_message(order_obj)
    order_chat_message_sender.send_message(order_chat_message)

    return Response(status_code=status.HTTP_201_CREATED)
