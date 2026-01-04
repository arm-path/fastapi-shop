from fastapi import HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import Select, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.warehouse.models import Supplier
from app.warehouse.schemas import SupplierCreateSchema, SupplierListSchema


class SupplierService:
    @classmethod
    async def list(cls, session: AsyncSession, inn, title) -> Page[SupplierListSchema]:
        supplier_query: Select = select(Supplier)
        if inn:
            supplier_query: Select = supplier_query.where(Supplier.inn == inn)
        if title:
            supplier_query: Select = supplier_query.where(Supplier.title.like(f'%{title}%'))
        return await paginate(session, supplier_query)

    @classmethod
    async def detail(cls, session: AsyncSession, supplier_id: int) -> Supplier:
        supplier = await session.get(Supplier, supplier_id)
        return supplier

    @classmethod
    async def create(cls, session: AsyncSession, data: SupplierCreateSchema) -> Supplier:
        supplier = Supplier(**data.model_dump())
        session.add(supplier)
        try:
            await session.commit()
        except IntegrityError as e:
            if e.orig.pgcode == '23505':
                raise HTTPException(status_code=400, detail='Supplier already exist.')
        return supplier

    @classmethod
    async def update(cls, session: AsyncSession, supplier_id: int, data: SupplierCreateSchema) -> Supplier:
        supplier = await session.get(Supplier, supplier_id)
        if not supplier:
            raise HTTPException(status_code=404, detail='Supplier not found.')
        supplier.title = data.title
        supplier.inn = data.inn
        supplier.address = data.address
        supplier.description = data.description
        try:
            await session.commit()
        except IntegrityError as e:
            if e.orig.pgcode == '23505':
                raise HTTPException(status_code=400, detail='Supplier already exist.')
        return supplier

    @classmethod
    async def delete(cls, session: AsyncSession, supplier_id: int) -> None:
        supplier = await session.get(Supplier, supplier_id)
        if not supplier:
            raise HTTPException(status_code=404, detail='Supplier not found.')
        await session.delete(supplier)
        await session.commit()
