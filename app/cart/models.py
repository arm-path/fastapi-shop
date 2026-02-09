from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, UniqueConstraint, CheckConstraint, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.settings.database import Base
from app.user.models import User

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

    __table_args__ = (
        UniqueConstraint('product_id', 'cart_id', name='uq_product_id_cart_id_cart_product'),
        CheckConstraint('quantity > 0', name='chk_quantity_cart_product'),
    )


@event.listens_for(User, 'after_insert')
def create_cart_user(mapper, connection, target):
    connection.execute(Cart.__table__.insert().values(user_id=target.id, ))