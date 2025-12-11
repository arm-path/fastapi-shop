from slugify import slugify
from sqlalchemy import String, event, ForeignKey, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.settings.database import Base


class Category(Base):
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    parent_id: Mapped[Category | None] = mapped_column(
        ForeignKey('category.id', ondelete='CASCADE'), nullable=True
    )


class Product(Base):
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    category_id: Mapped[Category] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    discount: Mapped[int] = mapped_column(Integer(), default=0)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)


@event.listens_for(Category, 'before_insert')
@event.listens_for(Category, 'before_update')
def generate_slug(mapper, connection, target):
    target.slug = slugify(target.title, max_length=255)
