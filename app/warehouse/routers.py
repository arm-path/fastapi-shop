from typing import Annotated

from fastapi import APIRouter, status, Query
from fastapi_pagination import Page

from app.settings.database import SessionDepends
from app.warehouse.schemas import SupplierCreateSchema, SupplierResponseSchema, SupplierListSchema
from app.warehouse.services import SupplierService

router = APIRouter(prefix='/warehouse', tags=['warehouse'])


@router.get('/supplier/list/', response_model=Page[SupplierListSchema])
async def supplier_list(session: SessionDepends,
                        inn: Annotated[int | None, Query(description='search parameters')] = None,
                        title: Annotated[str | None, Query(description='search parameters')] = None):
    return await SupplierService.list(session, inn, title)


@router.get('/supplier/{supplier_id}/detail/', response_model=SupplierResponseSchema)
async def supplier_detail(session: SessionDepends, supplier_id: int):
    return await SupplierService.detail(session, supplier_id)


@router.post('/supplier/create/', response_model=SupplierResponseSchema)
async def supplier_create(data: SupplierCreateSchema, session: SessionDepends):
    return await SupplierService.create(session, data)


@router.put('/supplier/{supplier_id}/update/', response_model=SupplierResponseSchema)
async def supplier_update(supplier_id: int, data: SupplierCreateSchema, session: SessionDepends):
    return await SupplierService.update(session, supplier_id, data)


@router.delete('/supplier/{supplier_id}/delete/', status_code=status.HTTP_204_NO_CONTENT)
async def supplier_delete(supplier_id: int, session: SessionDepends):
    return await SupplierService.delete(session, supplier_id)
