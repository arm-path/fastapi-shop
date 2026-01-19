from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cart.models import CartProduct
from app.cart.schemas import ProductCartCreateSchema, ProductCartResponseSchema
from app.product.models import Product
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
