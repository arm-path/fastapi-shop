from slugify import slugify
from sqlalchemy import String, event, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.settings.database import Base


class Category(Base):
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    parent_id: Mapped[Category | None] = mapped_column(
        ForeignKey('category.id', ondelete='CASCADE'), nullable=True
    )


@event.listens_for(Category, 'before_insert')
@event.listens_for(Category, 'before_update')
def generate_slug(mapper, connection, target):
    target.slug = slugify(target.title, max_length=255)
