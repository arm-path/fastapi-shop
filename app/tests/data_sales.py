from app.cart.schemas import ProductCartCreateSchema
from app.order.schemas import ProductOrderSchema
from app.supplies.schemas import SuppliesAddProductSchema

products_data_document_1 = [
    SuppliesAddProductSchema(product_id=1, quantity=5, price=12000.00),
    SuppliesAddProductSchema(product_id=2, quantity=10, price=10030.00),
    SuppliesAddProductSchema(product_id=3, quantity=15, price=9000.00),
]

products_data_document_2 = [
    SuppliesAddProductSchema(product_id=1, quantity=5, price=12000.00),
    SuppliesAddProductSchema(product_id=2, quantity=10, price=10030.00),
]

products_data_document_3 = [
    SuppliesAddProductSchema(product_id=2, quantity=5, price=12000.00),
    SuppliesAddProductSchema(product_id=3, quantity=25, price=10030.00),
]

order_1 = [
    ProductOrderSchema(product_id=1, quantity=2, price=15000.00),
    ProductOrderSchema(product_id=2, quantity=10, price=12030.00),
    ProductOrderSchema(product_id=3, quantity=15, price=11500.00),
]

order_2 = [ProductOrderSchema(product_id=2, quantity=5, price=12030.00),]

product_1_cart = ProductCartCreateSchema(product_id=1, quantity=2)
product_2_cart = ProductCartCreateSchema(product_id=2, quantity=10)
product_3_cart = ProductCartCreateSchema(product_id=3, quantity=15)

