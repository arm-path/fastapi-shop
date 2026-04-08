from app.order.services import OrderService
from app.product import Product
from app.supplies import Supplies
from app.supplies.services import SupplierService, SuppliesService
from app.tests.data_sales import (
    products_data_document_1,
    products_data_document_2, order_1, order_2, products_data_document_3,
)
from app.tests.data_supplies import (
    category_data,
    products_data,
    supplier_data_1,
    document_data_1,
    document_data_2, document_data_3
)
from app.user import User
from app.tests.test_user import test_create_user

async def test_preparatory_data(test_session):
    test_session.add(category_data)
    test_session.add_all(products_data)
    await test_session.commit()
    user = await test_session.get(User, 1)
    await SupplierService.create(test_session, supplier_data_1)
    await SuppliesService.create(test_session, user, document_data_1)
    await SuppliesService.create(test_session, user, document_data_2)
    await SuppliesService.create(test_session, user, document_data_3)


async def test_supplies_products_1(test_session):
    user = await test_session.get(User, 1)
    supplies_document_1 = await test_session.get(Supplies, 1)
    supplies_document_2 = await test_session.get(Supplies, 2)

    await SuppliesService.add_products(
        session=test_session,
        user=user,
        supplies_id=supplies_document_1.id,
        data=products_data_document_1
    )

    await SuppliesService.add_products(
        session=test_session,
        user=user,
        supplies_id=supplies_document_2.id,
        data=products_data_document_2
    )

    test_session.expire_all()

    product_1 = await test_session.get(Product, 1)
    product_2 = await test_session.get(Product, 2)
    product_3 = await test_session.get(Product, 3)

    assert product_1.quantity == 10  # PRODUCT-1 = 10
    assert product_2.quantity == 20  # PRODUCT-2 = 20
    assert product_3.quantity == 15  # PRODUCT-3 = 15


async def test_sales_products_1(test_session):
    user = await test_session.get(User, 1)
    await OrderService.create(session=test_session, user=user, data=order_1)

    product_1 = await test_session.get(Product, 1)
    product_2 = await test_session.get(Product, 2)
    product_3 = await test_session.get(Product, 3)

    assert product_1.quantity == 8  # PRODUCT-1: 10 - 2 = 8
    assert product_2.quantity == 10  # PRODUCT-2: = 20 - 10 = 10
    assert product_3.quantity == 0  # PRODUCT-3: = 15 - 15 = 0


async def test_sales_products_2(test_session):
    user = await test_session.get(User, 1)
    await OrderService.create(session=test_session, user=user, data=order_2)

    product_1 = await test_session.get(Product, 1)
    product_2 = await test_session.get(Product, 2)
    product_3 = await test_session.get(Product, 3)

    assert product_1.quantity == 8  # PRODUCT-1: 8
    assert product_2.quantity == 5  # PRODUCT-2: = 10 - 5 = 5
    assert product_3.quantity == 0  # PRODUCT-3: 0


async def test_supplies_products_2(test_session):
    user = await test_session.get(User, 1)
    supplies_document_3 = await test_session.get(Supplies, 3)

    await SuppliesService.add_products(
        session=test_session,
        user=user,
        supplies_id=supplies_document_3.id,
        data=products_data_document_3
    )

    test_session.expire_all()

    product_1 = await test_session.get(Product, 1)
    product_2 = await test_session.get(Product, 2)
    product_3 = await test_session.get(Product, 3)

    assert product_1.quantity == 8  # PRODUCT-1: 8
    assert product_2.quantity == 10  # PRODUCT-2: = 5 + 5 = 5
    assert product_3.quantity == 25  # PRODUCT-3: = 0 + 25

async def test_supplies_draft_products(test_session):
    supplies_document_3 = await test_session.get(Supplies, 3)

    supplies_document_3.draft = True

    test_session.commit()

    product_1 = await test_session.get(Product, 1)
    product_2 = await test_session.get(Product, 2)
    product_3 = await test_session.get(Product, 3)

    assert product_1.quantity == 8
    assert product_2.quantity == 5
    assert product_3.quantity == 0