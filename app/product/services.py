from typing import List, Sequence

from fastapi import HTTPException, status
from sqlalchemy import select, Result, Select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.exceptions import DataTypeException
from app.product.models import Category, Characteristic, Product, CharacteristicProduct
from app.product.schemas import (CategorySchema,
                                 CharacteristicSchema,
                                 ProductSchema,
                                 ProductCharacteristicSchema,
                                 ProductCharacteristicSchemaUpdate)
from app.utils import check_type


class CategoryService:

    @classmethod
    async def list(cls, session: AsyncSession, characteristics: bool) -> Sequence[Category]:
        category_query: Select = select(Category).where(Category.parent_id == None)
        if characteristics:
            category_query: Select = get_category_load_characteristic(category_query)
        category_result: Result = await session.execute(category_query)
        categories: Sequence[Category] = category_result.scalars().all()
        return categories

    @classmethod
    async def detail(cls, session: AsyncSession, category_id: int, characteristic: bool) -> Sequence[Category]:
        category_query: Select = (
            select(Category).where(Category.id == category_id).options(selectinload(Category.categories))
        )
        if characteristic:
            category_query: Select = get_category_load_characteristic(category_query)
        category_result: Result = await session.execute(category_query)
        categories: Sequence[Category] = category_result.scalar_one_or_none()
        return categories

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
    async def delete(cls, session: AsyncSession, category_id: int) -> None:
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail='Category not found.')
        await session.delete(category)
        await session.commit()

    @classmethod
    async def get_characteristic(cls, session: AsyncSession, category_id: int) -> Sequence[Characteristic]:
        characteristic_query: Select = select(Characteristic).where(Characteristic.category_id == category_id)
        characteristic_result: Result = await session.execute(characteristic_query)
        characteristics: Sequence[Characteristic] = characteristic_result.scalars().all()
        return characteristics

    @classmethod
    async def add_characteristic(cls,
                                 session: AsyncSession,
                                 category_id: int,
                                 data: List[CharacteristicSchema]) -> Sequence[Characteristic]:
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
        return await cls.get_characteristic(session, category_id)

    @classmethod
    async def update_characteristic(cls,
                                    session: AsyncSession,
                                    characteristic_id: int,
                                    data: CharacteristicSchema) -> Characteristic:
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
                                    ) -> None:
        characteristic = await session.get(Characteristic, characteristic_id)
        if not characteristic:
            raise HTTPException(status_code=404, detail='Characteristic not found.')
        await session.delete(characteristic)
        await session.commit()


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
        product = await session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Product not found')

        category_is_changed = product.category_id != data.category_id

        product.title = data.title
        product.category_id = data.category_id
        product.price = data.price
        product.discount = data.discount
        product.description = data.description

        try:
            if category_is_changed:
                product_characteristics_query = (
                    delete(CharacteristicProduct).where(CharacteristicProduct.product_id == product.id)
                )
                await session.execute(product_characteristics_query)
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
    async def delete(cls, session: AsyncSession, product_id: int):
        product = await session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Product not found.')
        await session.delete(product)
        product_characteristic_query = (
            delete(CharacteristicProduct).where(CharacteristicProduct.product_id == product.id)
        )
        await session.execute(product_characteristic_query)
        await session.commit()

    @classmethod
    async def add_characteristic(cls, session: AsyncSession, product_id: int, data: List[ProductCharacteristicSchema]):
        product_characteristic = []
        characteristic_ids = []
        for characteristic in data:
            product_characteristic.append(CharacteristicProduct(
                product_id=product_id,
                characteristic_id=characteristic.characteristic_id,
                value=characteristic.value
            ))
            characteristic_ids.append(characteristic.characteristic_id)

        characteristics_query: Select = select(Characteristic).where(Characteristic.id.in_(characteristic_ids))
        characteristic_result: Result[tuple[Characteristic]] = await session.execute(characteristics_query)
        characteristic_objects: Sequence[Characteristic] = characteristic_result.scalars().all()
        category_ids = []

        for obj in characteristic_objects:
            category_ids.append(obj.category_id)
            for characteristic in data:
                if characteristic.characteristic_id == obj.id and not check_type(obj.type, characteristic.value):
                    raise DataTypeException(obj.type, characteristic.__dict__)

        category_ids = list(set([obj.category_id for obj in characteristic_objects]))

        if len(category_ids) > 1:
            raise HTTPException(status_code=400, detail='Characteristics with different categories.')

        product = await session.get(Product, product_id)

        if not product:
            raise HTTPException(status_code=404, detail='Product not found.')

        if product.category_id != category_ids[0]:
            raise HTTPException(status_code=400, detail='Characteristics do not belong to the products.')

        try:
            session.add_all(product_characteristic)
            await session.commit()
        except IntegrityError as e:
            if e.orig.pgcode == '23503':
                message = e.orig.__cause__.__dict__['detail'].replace('(', '').replace(')', '').replace('"', '')
                raise HTTPException(status_code=400, detail=message)
            if e.orig.pgcode == '23505':
                raise HTTPException(status_code=400, detail='Duplication characteristic.')

    @classmethod
    async def update_characteristic(cls,
                                    session: AsyncSession,
                                    product_id: int,
                                    data: List[ProductCharacteristicSchemaUpdate]
                                    ):

        product_characteristic_ids = [characteristic.id for characteristic in data]
        product_characteristic_query: Select = (
            select(CharacteristicProduct)
            .where(CharacteristicProduct.id.in_(product_characteristic_ids),
                   CharacteristicProduct.product_id == product_id)
            .options(selectinload(CharacteristicProduct.characteristic))
        )

        product_characteristic_result: Result = await session.execute(product_characteristic_query)
        product_characteristic_obj: Sequence[CharacteristicProduct] = product_characteristic_result.scalars().all()

        for characteristic in data:
            for product_characteristic in product_characteristic_obj:
                if product_characteristic.id == characteristic.id:
                    if not check_type(product_characteristic.characteristic.type, characteristic.value):
                        raise DataTypeException(product_characteristic.characteristic.type, characteristic.__dict__)
                    product_characteristic.value = characteristic.value
                    break

        await session.commit()


def get_category_load_characteristic(query: Select):
    return query.options(
        selectinload(Category.characteristics)
        .load_only(Characteristic.id, Characteristic.title, Characteristic.type, Characteristic.unit)
    )
