from fastapi import APIRouter

from app.cart.schemas import ProductCartCreateSchema, ProductCartResponseSchema
from app.cart.services import CartService
from app.settings.database import SessionDepends
from app.user.services import CurrentUserDepends

router = APIRouter(
    prefix='/cart',
    tags=['cart']
)


@router.post('/add-product/', response_model=ProductCartResponseSchema)
async def add_product_to_cart(user: CurrentUserDepends, session: SessionDepends, data: ProductCartCreateSchema):
    return await CartService.add_product(user, session, data)
