import functools

import pytest
from fastapi import HTTPException

from app.supplies.services import SupplierService
from app.tests.conftest import error_session, assert_http_exception
from app.tests.data_supplies import (
    products_data,
    category_data,
    supplier_data_1, supplier_data_2, supplier_data_3, supplier_data_4)


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
