from fastapi import APIRouter

from app.routers.routers_v1.endpoints import order_payment_methods, orders


router = APIRouter()

router.include_router(order_payment_methods.router, tags=['Способы оплаты заказов'])
router.include_router(orders.router, tags=['Заказы'])
