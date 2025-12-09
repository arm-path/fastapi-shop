__all__ = (
    'router',
    'Category'
)

from fastapi import APIRouter

from .routers import category_router
from .routers import product_router
from .models import Category

router = APIRouter(tags=['Product'])
router.include_router(category_router)
router.include_router(product_router)
