from typing import Literal, List

from slugify import slugify
from sqlalchemy import String, event, ForeignKey, Numeric, Integer, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.settings.database import Base


class Category(Base):
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    parent_id: Mapped[Category | None] = mapped_column(
        ForeignKey('category.id', ondelete='CASCADE'), nullable=True
    )

    characteristics: Mapped[List['Characteristic']] = relationship(back_populates='category')


class Product(Base):
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    category_id: Mapped[Category] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    discount: Mapped[int] = mapped_column(Integer(), default=0)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)


class Characteristic(Base):
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    unit: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    type: Mapped[Literal['integer', 'float', 'string', 'boolean']] = mapped_column(
        ENUM('integer', 'float', 'string', 'boolean', name='enum_type_characteristic'),
    )

    category: Mapped['Category'] = relationship(back_populates='characteristics')

    __table_args__ = (
        UniqueConstraint('title', 'category_id', name='uq_tb-characteristic_title_category_id'),
    )


class CharacteristicProduct(Base):
    characteristic_id: Mapped[Characteristic] = mapped_column(ForeignKey('characteristic.id', ondelete='CASCADE'))
    product_id: Mapped[Product] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'))
    value: Mapped[str | None] = mapped_column(String(255), nullable=True)

    __table_args__ = (
        CheckConstraint(
            """
            EXISTS (
                SELECT 1
                FROM characteristic c
                JOIN product p ON p.id = characteristic_product.product_id
                WHERE c.id = characteristic_product.characteristic_id AND c.category_id = p.category_id
            )
            """,
            name='chk_characteristic_product_category_match'
        ),
        UniqueConstraint('characteristic_id', 'product_id', name='uq_characteristic_productl'),
    )


@event.listens_for(Category, 'before_insert')
@event.listens_for(Category, 'before_update')
def generate_slug(mapper, connection, target):
    target.slug = slugify(target.title, max_length=255)
