from typing import List

from fastapi import APIRouter

from app.product.schemas import (CategorySchema,
                                 CharacteristicSchema,
                                 ProductSchema,
                                 ProductCharacteristicSchema,
                                 ProductCharacteristicSchemaUpdate,
                                 CategoryItemSchema,
                                 CategoryWithCharacteristicSchema, CategoryDetailSchema,
                                 CategoryDetailWithCharacteristicSchema)
from app.product.services import CategoryService, ProductService
from app.settings.database import SessionDepends

category_router = APIRouter(prefix='/category')
product_router = APIRouter(prefix='/product')


@category_router.get('/list/',
                     response_model=List[CategoryItemSchema] | List[CategoryWithCharacteristicSchema])
async def category_list(session: SessionDepends, characteristics: bool | None = None):
    return await CategoryService.list(session, characteristics)


@category_router.get('/detail/{category_id}/',
                     response_model=CategoryDetailSchema | CategoryDetailWithCharacteristicSchema)
async def category_detail(category_id: int, session: SessionDepends, characteristics: bool | None = None):
    return await CategoryService.detail(session, category_id, characteristics)


@category_router.post('/create')
async def category_create(data: CategorySchema, session: SessionDepends):
    return await CategoryService.create(session, data)


@category_router.put('/update/{category_id}')
async def category_update(category_id: int, data: CategorySchema, session: SessionDepends):
    return await CategoryService.update(session, category_id, data)


@category_router.delete('/delete/{category_id}')
async def category_delete(category_id: int, session: SessionDepends):
    await CategoryService.delete(session, category_id)


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


@product_router.post('/create')
async def create_product(data: ProductSchema, session: SessionDepends):
    return await ProductService.create(session, data)


@product_router.put('/update/{product_id}')
async def update_product(data: ProductSchema, product_id: int, session: SessionDepends):
    return await ProductService.update(session, product_id, data)


@product_router.delete('/delete/{product_id}')
async def delete_product(product_id: int, session: SessionDepends):
    return await ProductService.delete(session, product_id)


@product_router.post('/create-characteristics/{product_id}')
async def create_product_characteristic(product_id: int,
                                        data: List[ProductCharacteristicSchema],
                                        session: SessionDepends
                                        ):
    return await ProductService.add_characteristic(session, product_id, data)


@product_router.post('/update-characteristics/{product_id}')
async def update_product_characteristic(product_id: int,
                                        data: List[ProductCharacteristicSchemaUpdate],
                                        session: SessionDepends):
    return await ProductService.update_characteristic(session, product_id, data)
