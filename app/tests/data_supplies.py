from app.product import Product, Category
from app.supplies.schemas import SupplierCreateSchema

category_data = Category(title='category-1')

products_data = [
    Product(title='product-1', category_id=1, price=15000.00),
    Product(title='product-2', category_id=1, price=12030.00),
    Product(title='product-3', category_id=1, price=11500.00)
]


supplier_data_1 = SupplierCreateSchema(
    title='supplier-1',
    inn='172873981736',
    address='',
    description=''
)

supplier_data_2 = SupplierCreateSchema(
    title='supplier-2',
    inn='272473981736',
    address='',
    description=''
)

supplier_data_3 = SupplierCreateSchema(
    title='supplier-3',
    inn='372473981736',
    address='',
    description=''
)

supplier_data_4 = SupplierCreateSchema(
    title='supplier-4',
    inn='472473981736',
    address='',
    description=''
)