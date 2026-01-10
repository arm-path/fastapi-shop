from datetime import date, datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import (ForeignKey,
                        Integer,
                        String,
                        Date,
                        text,
                        DECIMAL,
                        Computed,
                        Boolean,
                        UniqueConstraint,
                        CheckConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.settings.database import Base

if TYPE_CHECKING:
    from app.product import Product


class Warehouse(Base):
    title: Mapped[str] = mapped_column(String(91), unique=True, nullable=False)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)


class WarehouseProduct(Base):
    warehouse_id: Mapped[int] = mapped_column(
        ForeignKey('warehouse.id', ondelete='RESTRICT'),
        index=True, unique=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey('product.id', ondelete='RESTRICT'),
        index=True, unique=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    product: Mapped[Product] = relationship(back_populates='warehouses')

    __table_args__ = (CheckConstraint('quantity > 0', name='chk_warehouse_product_quantity'),)


class Supplier(Base):
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    inn: Mapped[str] = mapped_column(String(12), unique=True, index=True, nullable=False)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    documents: Mapped[List['Supplies']] = relationship(back_populates='supplier')

    __table_args__ = (CheckConstraint("inn ~ '^[0-9]*$'", name='chk_supplier_inn'),)


class Supplies(Base):
    document_number: Mapped[str] = mapped_column(String(61), nullable=False)
    supplier_id: Mapped[int] = mapped_column(ForeignKey('supplier.id', ondelete='RESTRICT'), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey('warehouse_product.id', ondelete='RESTRICT'))
    document_data: Mapped[date] = mapped_column(Date, nullable=False)
    created: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow)
    create_user_id: Mapped[int | None] = mapped_column(ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    update_user_id: Mapped[int | None] = mapped_column(ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    draft: Mapped[bool] = mapped_column(Boolean, default=False)

    supplier: Mapped['Supplier'] = relationship(back_populates='documents')
    products: Mapped[List['SuppliesProduct']] = relationship(back_populates='supplies')


class SuppliesProduct(Base):
    supplies_id: Mapped[int] = mapped_column(ForeignKey('supplies.id', ondelete='CASCADE'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='RESTRICT'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    total: Mapped[float] = mapped_column(DECIMAL(10, 2), Computed(price * quantity))

    supplies: Mapped['Supplies'] = relationship(back_populates='products')
    supplies_product: Mapped['Product'] = relationship(back_populates='supplies_documents')

    __table_args__ = (
        UniqueConstraint('supplies_id', 'product_id', name='uq_supplies_product__supplies_product'),
        CheckConstraint('price > 0', name='chk_supplies_product_price'),
        CheckConstraint('quantity > 0', name='chk_supplies_product_quantity')
    )
