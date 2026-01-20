from typing import TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.cart.models import CartProduct
from app.cart.schemas import ProductCartCreateSchema, ProductCartResponseSchema
from app.product.models import Product

if TYPE_CHECKING:
    from app.user import User

class CartService:
    @classmethod
    async def add_product(cls,
                          user: User,
                          session: AsyncSession,
                          data: ProductCartCreateSchema) -> ProductCartResponseSchema:

        await session.refresh(user, ['cart'])

        product_query = (
            select(Product, CartProduct)  # Возвращаем и Product, и CartProduct (может быть None)
            .join(
                CartProduct,
                (CartProduct.product_id == Product.id) & (CartProduct.cart_id == user.cart.id),
                isouter=True
            )
            .where(Product.id == data.product_id)
        )

        product_result = await session.execute(product_query)
        product, cart_product = product_result.one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail='Product not found')
        if product.quantity < data.quantity:
            raise HTTPException(status_code=400, detail='Product not enough')

        if not cart_product:
            product_in_cart = CartProduct(cart_id=user.cart.id, product_id=data.product_id, quantity=data.quantity)
            session.add(product_in_cart)
        else:
            if product.quantity < cart_product.quantity + data.quantity:
                raise HTTPException(status_code=400, detail='Product not enough')
            cart_product.quantity = cart_product.quantity + data.quantity
            product_in_cart = cart_product
        await session.commit()
        return product_in_cart

    @classmethod
    async def edit_product(cls, user: User, session: AsyncSession, product_id: int, quantity: int):
        await session.refresh(user, ['cart'])

        product_query = (
            select(Product, CartProduct)
            .join(
                CartProduct,
                (CartProduct.product_id == Product.id) & (CartProduct.cart_id == user.cart.id),
                isouter=True
            )
            .where(Product.id == product_id)
        )

        product_result = await session.execute(product_query)
        product, cart_product = product_result.one_or_none()

        if not product or product.quantity < quantity:
            raise HTTPException(status_code=404, detail='Product not found or not enough')
        if not cart_product:
            raise HTTPException(status_code=400, detail='Product not exist in cart')

        cart_product.quantity = quantity
        await session.commit()
        return cart_product

    @classmethod
    async def delete_product(cls, session: AsyncSession, user: User, product_id: int) -> None:
        await session.refresh(user, ['cart'])

        product_cart_query = (
            delete(CartProduct)
            .where(CartProduct.product_id == product_id, CartProduct.cart_id == user.cart.id)
        )

        await session.execute(product_cart_query)
        await session.commit()
