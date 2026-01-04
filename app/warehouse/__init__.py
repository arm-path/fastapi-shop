__all__ =(
    'router',
    'Warehouse',
    'Supplies',
    'Supplier',
    'SuppliesProduct'
)

from app.warehouse.models import Warehouse, Supplies, Supplier, SuppliesProduct
from app.warehouse.routers import router