from typing import List

from fastapi import APIRouter

from app.order.schemas import ProductOrderSchema
from app.order.services import OrderService
from app.settings.database import SessionDepends
from app.user.services import CurrentUserDepends

router = APIRouter(
    prefix='/order',
    tags=['order']
)


@router.post('/create/')
async def create_order(session: SessionDepends, user: CurrentUserDepends, data: List[ProductOrderSchema]):
    await OrderService.create(session, user, data)