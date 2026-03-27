import functools

from app.product.services import ProductService
from app.supplies import SuppliesProduct
from app.supplies.services import SupplierService, SuppliesService
from app.tests.conftest import assert_http_exception
from app.tests.data_supplies import (
    products_data,
    category_data,
    supplier_data_1, supplier_data_2, supplier_data_3, supplier_data_4,
    document_data_1, document_data_2, products_data_document_1_product_1, products_data_document_2_product_1,
    products_data_document_2_product_2, products_data_document_1_product_2, products_data_document_1_not_found,
    products_data_document_1_product_1_update, document_data_2_draft
)
from app.tests.test_user import test_create_user
from app.user import User


async def test_create_products(test_session):
    test_session.add(category_data)
    test_session.add_all(products_data)
    await test_session.commit()


async def test_supplier_service(test_session):
    supplier_data_5 = supplier_data_4.model_copy()
    supplier_1 = await SupplierService.create(test_session, supplier_data_1)
    supplier_2 = await SupplierService.create(test_session, supplier_data_2)
    supplier_3 = await SupplierService.create(test_session, supplier_data_3)
    supplier_4 = await SupplierService.create(test_session, supplier_data_4)

    assert supplier_1.id == 1 and supplier_2.id == 2 and supplier_3.id == 3 and supplier_4.id == 4

    await assert_http_exception(
        functools.partial(SupplierService.create, None, supplier_data_1),
        expected_message='Supplier already exist'
    )

    supplier_data_5.inn = supplier_data_2.inn
    await assert_http_exception(
        functools.partial(SupplierService.update, None, 4, supplier_data_5),
        expected_message='Supplier already exist'
    )


async def test_supplies_products(test_session):
    user = await test_session.get(User, 1)
    supplies_document_1 = await SuppliesService.create(test_session, user, document_data_1)
    supplies_document_2 = await SuppliesService.create(test_session, user, document_data_2)
    assert supplies_document_1.id == 1 and supplies_document_2.id == 2

    await SuppliesService.add_products(
        session=test_session,
        user=user,
        supplies_id=supplies_document_1.id,
        data=[products_data_document_1_product_1]
    )

    product_1 = await ProductService.detail(test_session, product_id=1)
    assert product_1.quantity == products_data_document_1_product_1.quantity

    await SuppliesService.add_products(
        session=test_session,
        user=user,
        supplies_id=supplies_document_2.id,
        data=[products_data_document_2_product_1, products_data_document_2_product_2]
    )

    await test_session.refresh(product_1)  # Очищаем кэш сессии для получения актуальных данных

    product_1 = await ProductService.detail(test_session, product_id=1)
    product_2 = await ProductService.detail(test_session, product_id=2)
    assert product_1.quantity == products_data_document_2_product_1.quantity + products_data_document_1_product_1.quantity
    assert product_2.quantity == products_data_document_2_product_2.quantity

    await SuppliesService.add_products(
        session=test_session,
        user=user,
        supplies_id=supplies_document_1.id,
        data=[products_data_document_1_product_2]
    )

    await test_session.refresh(product_2)  # Очищаем кэш сессии для получения актуальных данных
    product_2 = await ProductService.detail(test_session, product_id=2)
    assert product_2.quantity == products_data_document_2_product_2.quantity + products_data_document_1_product_2.quantity

    await assert_http_exception(
        functools.partial(
            SuppliesService.add_products, None, user, supplies_document_1.id, [products_data_document_1_product_2]
        ),
        expected_message='Violation unique product_id & supplies_id.'
    )

    await assert_http_exception(
        functools.partial(
            SuppliesService.add_products, None, user, supplies_document_1.id, [products_data_document_1_not_found]
        ),
        expected_message='Product not found.'
    )

    document_product = await test_session.get(SuppliesProduct, 1)

    assert document_product.id == 1
    assert document_product.product_id == products_data_document_1_product_1.product_id
    assert document_product.quantity == products_data_document_1_product_1.quantity

    await SuppliesService.update_product(
        session=test_session,
        user=user,
        supplies_product_id=document_product.id,
        data=products_data_document_1_product_1_update
    )

    await test_session.refresh(product_1)  # Очищаем кэш сессии для получения актуальных данных
    product_1 = await ProductService.detail(test_session, product_id=1)
    assert product_1.quantity == products_data_document_1_product_1_update.quantity + products_data_document_2_product_1.quantity

    await SuppliesService.delete_product(test_session, document_product.id)
    await test_session.refresh(product_1)  # Очищаем кэш сессии для получения актуальных данных
    product_1 = await ProductService.detail(test_session, product_id=1)
    assert product_1.quantity == products_data_document_2_product_1.quantity

    await SuppliesService.update(test_session, user, supplies_document_2.id, document_data_2_draft)

    await test_session.refresh(product_1)  # Очищаем кэш сессии для получения актуальных данных
    await test_session.refresh(product_2)  # Очищаем кэш сессии для получения актуальных данных
    product_1 = await ProductService.detail(test_session, product_id=1)
    product_2 = await ProductService.detail(test_session, product_id=2)
    assert product_1.quantity == 0
    assert product_2.quantity == products_data_document_1_product_2.quantity

    await SuppliesService.update(test_session, user, supplies_document_2.id, document_data_2)

    await test_session.refresh(product_1)  # Очищаем кэш сессии для получения актуальных данных
    await test_session.refresh(product_2)  # Очищаем кэш сессии для получения актуальных данных
    product_1 = await ProductService.detail(test_session, product_id=1)
    product_2 = await ProductService.detail(test_session, product_id=2)
    assert product_1.quantity == products_data_document_2_product_1.quantity
    assert product_2.quantity == products_data_document_1_product_2.quantity + products_data_document_2_product_2.quantity
