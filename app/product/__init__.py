__all__ = (
    'router',
    'Category',
    'Product',
    'Characteristic',
    'CharacteristicProduct'
)

from fastapi import APIRouter

from .models import Category, Product, Characteristic, CharacteristicProduct
from .routers import category_router
from .routers import product_router

router = APIRouter(tags=['Product'])
router.include_router(category_router)
router.include_router(product_router)
