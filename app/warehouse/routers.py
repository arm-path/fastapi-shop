from typing import Annotated

from fastapi import APIRouter, status, Query
from fastapi_pagination import Page

from app.settings.database import SessionDepends
from app.user.services import InstallerUserDepends
from app.warehouse.schemas import SupplierCreateSchema, SupplierResponseSchema, SupplierListSchema, SuppliesSchema, \
    SuppliesBaseResponseSchema
from app.warehouse.services import SupplierService, SuppliesService

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


@router.post('/supplies/create-document/', response_model=SuppliesBaseResponseSchema)
async def supplies_create(session: SessionDepends, user: InstallerUserDepends, data: SuppliesSchema):
    return await SuppliesService.create(session, user, data)


@router.put('/supplies/{supplies_id}/update-document/', response_model=SuppliesBaseResponseSchema)
async def supplies_update(session: SessionDepends, user: InstallerUserDepends, supplies_id: int, data: SuppliesSchema):
    return await SuppliesService.update(session, user, supplies_id, data)


@router.delete('/supplies/{supplies_id}/delete-document/', status_code=status.HTTP_204_NO_CONTENT)
async def supplies_delete(session: SessionDepends, user: InstallerUserDepends, supplies_id: int):
    await SuppliesService.delete(session, user, supplies_id)
