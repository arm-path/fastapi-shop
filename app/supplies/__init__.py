__all__ = (
    'router',
    'Supplies',
    'Supplier',
    'SuppliesProduct'
)

from app.supplies.models import Supplies, Supplier, SuppliesProduct
from app.supplies.routers import router
