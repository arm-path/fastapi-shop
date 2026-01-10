from datetime import datetime
from typing import Literal, get_args

from sqlalchemy import ForeignKey, Integer, DECIMAL, Computed, CheckConstraint, DateTime, text, Boolean, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.settings.database import Base

ORDER_STATUS = Literal['accepted', 'assembled', 'moving warehouse', 'delivery', 'delivered', 'completed', 'cancelled']


class Station(Base):
    address: Mapped[str] = mapped_column(String(255), index=True, nullable=False)


class Order(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    station_id: Mapped[int | None] = mapped_column(ForeignKey('station.id', ondelete='SET NULL'), nullable=True)
    created: Mapped[datetime] = mapped_column(DateTime, server_default=text("TIMEZONE('utc', now())"))
    updated: Mapped[datetime] = mapped_column(DateTime, server_default=text("TIMEZONE('utc', now())"), onupdate=True)
    status: Mapped[ORDER_STATUS] = mapped_column(
        ENUM(*list(get_args(ORDER_STATUS)), name='enum_order_status'),
        default='accepted', nullable=False
    )
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
