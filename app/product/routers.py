from fastapi import APIRouter

from app.product.schemas import CategorySchema
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
