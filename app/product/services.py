from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.product.models import Category, Characteristic, Product
from app.product.schemas import CategorySchema, CharacteristicSchema, ProductSchema


class CategoryService:
    @classmethod
    async def create(cls, session: AsyncSession, data: CategorySchema) -> Category:
        category = Category(**data.model_dump())
        try:
            session.add(category)
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail='Category already exists.')
        return category

    @classmethod
    async def update(cls, session: AsyncSession, category_id: int, data: CategorySchema) -> Category:
        category = await session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail='Category not found.')
        category.title = data.title
        category.parent_id = data.parent_id
        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail='Category already exists.')
        return category

    @classmethod
    async def delete(cls, session: AsyncSession, category_id: int):
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail='Category not found.')
        await session.delete(category)
        await session.commit()

    @classmethod
    async def add_characteristic(cls,
                                 session: AsyncSession,
                                 category_id: int,
                                 data: List[CharacteristicSchema]):
        instances = []
        for instance in data:
            instances.append(Characteristic(category_id=category_id, **instance.model_dump()))
        try:
            session.add_all(instances)
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            if e.orig.pgcode == '23503':
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category not found.')
            if e.orig.pgcode == '23505':
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Violation unique characteristics.')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unhandled exception.')
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error.')

    @classmethod
    async def update_characteristic(cls,
                                    session: AsyncSession,
                                    characteristic_id: int,
                                    data: CharacteristicSchema):
        characteristic = await session.get(Characteristic, characteristic_id)
        if not characteristic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Characteristic not found.')
        characteristic.title = data.title
        characteristic.unit = data.unit
        characteristic.type = data.type
        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Characteristic already exists.')
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error.')
        return characteristic

    @classmethod
    async def delete_characteristic(cls,
                                    session: AsyncSession,
                                    characteristic_id: int
                                    ):
        characteristic = await session.get(Characteristic, characteristic_id)
        if not characteristic:
            raise HTTPException(status_code=404, detail='Characteristic not found.')
        await session.delete(characteristic)
        await session.commit()

    @classmethod
    async def detail(cls, session: AsyncSession, category_id):
        query = (
            select(Category)
            .where(Category.id == category_id)
            .options(selectinload(Category.characteristics))
        )
        category: Result[tuple[Category]] = await session.execute(query)
        category: Category | None = category.scalar_one_or_none()
        return category


class ProductService:
    @classmethod
    async def create(cls, session: AsyncSession, data: ProductSchema) -> Product:
        product = Product(**data.model_dump())
        try:
            session.add(product)
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            if e.orig.pgcode == '23503':
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category not found.')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unhandled exception.')
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error.')
        return product

    @classmethod
    async def update(cls, session: AsyncSession, product_id: int, data: ProductSchema):
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Product not found')

        category_is_changed = product.category_id != data.category_id

        product.title = data.title
        product.category_id = data.category_id
        product.price = data.price
        product.discount = data.discount
        product.description = data.description

        #   TODO: category_is_changed: CharacteristicProduct delete by product_id.

        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            if e.orig.pgcode == '23503':
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category not found.')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unhandled exception.')
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error.')

    @classmethod
    async def delete(cls, session: AsyncSession, product_id: int):
        product = await session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Product not found.')
        await session.delete(product)
        # TODO: CharacteristicProduct delete by product_id.
        await session.commit()
