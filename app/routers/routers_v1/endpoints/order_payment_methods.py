from typing import List

from fastapi import APIRouter

from app.repos.order_payment_methods import OrderPaymentMethodRepo
from app.schemas.order_payment_methods import OrderPaymentMethodSchema


router = APIRouter()


@router.get('/order-payment-methods', response_model=List[OrderPaymentMethodSchema])
async def get_order_payment_methods_list():
    '''Получить список способов оплаты заказа
    \f
    Returns:
    -----------------------
    order_payment_method_objects: ProductModel object
        список объектов способов оплаты заказа

    '''
    order_payment_method_objects = await OrderPaymentMethodRepo().get_objects()

    return order_payment_method_objects
