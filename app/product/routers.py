from typing import List

from fastapi import APIRouter

from app.product.schemas import CategorySchema, CharacteristicSchema
from app.product.services import CategoryService
from app.settings.database import SessionDepends

category_router = APIRouter(prefix='/category')
product_router = APIRouter(prefix='/product')


@category_router.post('/create')
async def category_create(data: CategorySchema, session: SessionDepends):
    return await CategoryService.create(session, data)


@category_router.put('/update/{category_id}')
async def category_update(category_id: int, data: CategorySchema, session: SessionDepends):
    return await CategoryService.update(session, category_id, data)


@category_router.post('/create-characteristics/{category_id}')
async def create_characteristics(category_id: int,
                                 data: List[CharacteristicSchema],
                                 session: SessionDepends):
    await CategoryService.add_characteristic(session, category_id, data)


@category_router.put('/update-characteristic/{characteristic_id}')
async def update_characteristics(characteristic_id: int,
                                 data: CharacteristicSchema,
                                 session: SessionDepends
                                 ):
    return await CategoryService.update_characteristic(session, characteristic_id, data)


@category_router.delete('/delete-characteristic/{characteristic_id}')
async def delete_characteristic(characteristic_id: int, session: SessionDepends):
    await CategoryService.delete_characteristic(session, characteristic_id)


@category_router.get('/detail/{category_id}')
async def category_detail(category_id: int, session: SessionDepends):
    return await CategoryService.detail(session, category_id)
