from datetime import datetime
from typing import Literal, get_args

from sqlalchemy import ForeignKey, Integer, DECIMAL, Computed, CheckConstraint, DateTime, text, Boolean
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.settings.database import Base

ORDER_STATUS_TYPE = Literal['accepted', 'assembled', 'delivery', 'completed', 'cancelled']
ORDER_STATUS = [*list(get_args(ORDER_STATUS_TYPE))]


class Order(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    created: Mapped[datetime] = mapped_column(DateTime, server_default=text("TIMEZONE('utc', now())"))
    updated: Mapped[datetime] = mapped_column(DateTime, server_default=text("TIMEZONE('utc', now())"), onupdate=True)
    status: Mapped[ORDER_STATUS_TYPE | None] = mapped_column(ENUM(*ORDER_STATUS, name='enum_order_status'),
                                                             nullable=True)
    is_payment: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class OrderProduct(Base):
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='RESTRICT'))
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id', ondelete='CASCADE'))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    total: Mapped[float] = mapped_column(DECIMAL(10, 2), Computed(quantity * price))

    __table_args__ = (
        CheckConstraint('quantity > 0', name='chk_order_product_quantity'),
        CheckConstraint('price > 0', name='chk_order_product_price')
    )
