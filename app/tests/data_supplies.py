from app.product import Product, Category
from app.supplies.schemas import SupplierCreateSchema, SuppliesSchema, SuppliesAddProductSchema

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

document_data_1 = SuppliesSchema(
    document_number='D1',
    document_data='2025-03-05',
    supplier_id=1,
    draft=False
)

document_data_2 = SuppliesSchema(
    document_number='D2',
    document_data='2025-03-08',
    supplier_id=1,
    draft=False
)

document_data_3 = SuppliesSchema(
    document_number='D3',
    document_data='2025-03-09',
    supplier_id=1,
    draft=False
)

products_data_document_1_product_1 = SuppliesAddProductSchema(
    product_id=1,
    quantity=3,
    price=12000.00
)

products_data_document_2_product_1 = SuppliesAddProductSchema(
    product_id=1,
    quantity=2,
    price=10000.00
)

products_data_document_2_product_2 = SuppliesAddProductSchema(
    product_id=2,
    quantity=5,
    price=10000.00
)

products_data_document_1_product_2 = SuppliesAddProductSchema(
    product_id=2,
    quantity=10,
    price=10000.00
)

products_data_document_1_not_found = SuppliesAddProductSchema(
    product_id=12,
    quantity=10,
    price=10000.00
)

document_data_2_draft = SuppliesSchema(
    document_number='D2',
    document_data='2025-03-08',
    supplier_id=1,
    draft=True
)

products_data_document_1_product_1_update = SuppliesAddProductSchema(
    product_id=1,
    quantity=5,
    price=12000.00
)
