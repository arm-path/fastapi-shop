

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.product.models import Category
from app.product.schemas import CategorySchema


class CategoryService:
    @classmethod
    async def create(cls, session: AsyncSession, data: CategorySchema) -> Category:
        category = Category(**data.model_dump())
        try:
            session.add(category)
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail='Category already exists!')
        return category

    @classmethod
    async def update(cls, session: AsyncSession, category_id: int, data: CategorySchema) -> Category:
        category = await session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail='Category not found!')
        category.title = data.title
        category.parent_id = data.parent_id
        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail='Category already exists!')
        return category