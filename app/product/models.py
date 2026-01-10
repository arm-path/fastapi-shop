from typing import Literal, List, TYPE_CHECKING

from slugify import slugify
from sqlalchemy import String, event, ForeignKey, Numeric, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.settings.database import Base

if TYPE_CHECKING:
    from app.warehouse.models import SuppliesProduct
    from app.warehouse.models import WarehouseProduct

CHARACTERISTIC_TYPE: list[str] = ['integer', 'float', 'string', 'boolean']


class Category(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    parent_id: Mapped[Category | None] = mapped_column(
        ForeignKey('category.id', ondelete='CASCADE'),
        index=True, nullable=True
    )

    characteristics: Mapped[List['Characteristic']] = relationship(back_populates='category')
    parent: Mapped['Category'] = relationship('Category', remote_side=[id], back_populates='categories')
    categories: Mapped[List['Category']] = relationship('Category', back_populates='parent')


class Product(Base):
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    category_id: Mapped[Category] = mapped_column(
        ForeignKey('category.id', ondelete='CASCADE'),
        index=True, nullable=False
    )
    price: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    characteristics: Mapped[List['CharacteristicProduct']] = relationship(back_populates='product')
    supplies_documents: Mapped[List['SuppliesProduct']] = relationship(back_populates='supplies_product')
    warehouses: Mapped[List[WarehouseProduct]] = relationship(back_populates='product')

    __table_args__ = (CheckConstraint('price > 0', name='chk_product_price'),)


class Characteristic(Base):
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey('category.id', ondelete='CASCADE'),
        index=True, nullable=False
    )
    unit: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    type: Mapped[Literal['integer', 'float', 'string', 'boolean']] = mapped_column(
        ENUM(*CHARACTERISTIC_TYPE, name='enum_characteristic_type')
    )

    category: Mapped['Category'] = relationship(back_populates='characteristics')
    product_values: Mapped[List['CharacteristicProduct']] = relationship(back_populates='characteristic')

    __table_args__ = (
        UniqueConstraint('title', 'category_id', name='uq_tb-characteristic_title_category_id'),
    )


class CharacteristicProduct(Base):
    characteristic_id: Mapped[Characteristic] = mapped_column(
        ForeignKey('characteristic.id', ondelete='CASCADE'),
        index=True, nullable=False
    )
    product_id: Mapped[Product] = mapped_column(
        ForeignKey('product.id', ondelete='CASCADE'),
        index=True, nullable=False
    )
    value: Mapped[str | None] = mapped_column(String(255), nullable=True)

    characteristic: Mapped['Characteristic'] = relationship(back_populates='product_values')
    product: Mapped['Product'] = relationship(back_populates='characteristics')

    __table_args__ = (
        UniqueConstraint('characteristic_id', 'product_id', name='uq_characteristic_product'),
    )


@event.listens_for(Category, 'before_insert')
@event.listens_for(Category, 'before_update')
def generate_slug_category(mapper, connection, target):
    target.slug = slugify(target.title, max_length=255)


@event.listens_for(Product, 'before_insert')
@event.listens_for(Product, 'before_update')
def generate_slug_product(mapper, connection, target):
    target.slug = slugify(target.title, max_length=255)
