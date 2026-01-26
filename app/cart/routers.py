from fastapi import APIRouter

from app.cart.schemas import ProductCartCreateSchema, ProductCartResponseSchema, ProductCartEditSchema, \
    CartResponseSchema
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


@router.put('/edit-product/{product_id}/', response_model=ProductCartResponseSchema)
async def edit_product_in_cart(user: CurrentUserDepends,
                               session: SessionDepends,
                               product_id: int,
                               data: ProductCartEditSchema):
    return await CartService.edit_product(user, session, product_id, data.quantity)


@router.delete('/delete-product/{product_id}/')
async def delete_product_in_cart(user: CurrentUserDepends, session: SessionDepends, product_id: int):
    return await CartService.delete_product(session, user, product_id)


@router.get('/detail/', response_model=CartResponseSchema)
async def detail_cart(user: CurrentUserDepends, session: SessionDepends):
    return await CartService.detail_cart(session, user)