from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.settings.database import Base

if TYPE_CHECKING:
    from app.product.models import Product
    from app.user.models import User


class Cart(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), unique=True)

    user: Mapped[User] = relationship(back_populates='cart')
    products: Mapped[List[CartProduct]] = relationship(back_populates='cart')


class CartProduct(Base):
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id', ondelete='CASCADE'))

    product: Mapped[Product] = relationship(back_populates='in_carts')
    cart: Mapped[Cart] = relationship(back_populates='products')
