import pytest
from fastapi import HTTPException
from sqlalchemy import select, func

from app.product import Category, Product, Characteristic, CharacteristicProduct
from app.product.services import CategoryService, ProductService
from app.tests.data_product import (
    category_data_1, category_data_2, category_data_3, category_data_4, category_data_5, category_data_update,
    characteristic_data_1, characteristic_data_2, characteristic_data_3, characteristic_data_4,
    product_data_1, product_data_2, product_data_3, product_data_4, product_data_5,
    characteristic_value_type_err, characteristic_category_err, characteristic_id_err, characteristic_1_c_1_product_1,
    characteristic_1_c_2_product_1, characteristic_update_type_err, characteristic_update

)


@pytest.mark.asyncio
async def test_category(test_session):
    c1 = await CategoryService.create(test_session, category_data_1)
    c2 = await CategoryService.create(test_session, category_data_2)
    c3 = await CategoryService.create(test_session, category_data_3)

    assert c1.id == 1 and c2.title == 'Category-2' and c3.parent_id == 1 and c1.slug == 'category-1'

    categories_query = await test_session.execute(select(Category))
    categories_result = categories_query.scalars().all()

    assert len(categories_result) == 3

    try:
        await CategoryService.create(test_session, category_data_4)
        assert False
    except HTTPException as e:
        assert '400: Category already exists.' in str(e)

    try:
        await CategoryService.create(test_session, category_data_3)
        assert False
    except HTTPException as e:
        assert '400: Category already exists.' in str(e)

    c6 = await CategoryService.create(test_session, category_data_5)

    assert c6.slug == 'category-3-2' and c6.id == 6

    c6 = await CategoryService.update(test_session, 6, category_data_update)

    assert c6.title == 'Category-4'

    await CategoryService.delete(test_session, 6)

    c6 = await CategoryService.detail(test_session, 6, False)

    assert c6 is None

    categories_query = await test_session.execute(select(Category))
    categories_result = categories_query.scalars().all()
    assert len(categories_result) == 3

    categories = await CategoryService.list(test_session, False)
    assert len(categories) == 2  # With parent_id == None


@pytest.mark.asyncio
async def test_characteristic(test_session):
    characteristics_category = [characteristic_data_1, characteristic_data_2, characteristic_data_3]
    await CategoryService.add_characteristic(test_session, 1, characteristics_category)

    category = await CategoryService.detail(test_session, 1, True)

    assert len(category.characteristics) == 3

    characteristics_category = [characteristic_data_4, characteristic_data_1]

    try:
        await CategoryService.add_characteristic(test_session, 1, characteristics_category)
        assert False
    except HTTPException as e:
        assert '400: Violation unique characteristics' in str(e)

    characteristics_category = [characteristic_data_4, ]

    await CategoryService.add_characteristic(test_session, 2, characteristics_category)

    category_2_characteristics = await CategoryService.get_characteristic(test_session, 2)

    assert len(category_2_characteristics) == 1 and category_2_characteristics[0].id == 6

    category_1_characteristics = await CategoryService.get_characteristic(test_session, 1)

    assert category_1_characteristics[0].id == 1

    characteristic = await CategoryService.update_characteristic(test_session, 1, characteristic_data_4)

    assert characteristic.title == 'characteristic 4'

    await CategoryService.delete_characteristic(test_session, 1)

    category = await CategoryService.detail(test_session, 1, True)

    assert len(category.characteristics) == 2


@pytest.mark.asyncio
async def test_product(test_session):
    product = await ProductService.create(test_session, product_data_1)
    assert product.id == 1 and product.title == product_data_1.title and product.price == product_data_1.price

    await ProductService.create(test_session, product_data_2)
    await ProductService.create(test_session, product_data_3)

    product_count = await test_session.execute(select(func.count()).select_from(Product))
    assert product_count.scalar() == 3

    with pytest.raises(HTTPException) as exc_info:
        await ProductService.create(test_session, product_data_4)
    assert exc_info.value.status_code == 400 and 'Category not found' in exc_info.value.detail

    with pytest.raises(HTTPException) as exc_info:
        await ProductService.create(test_session, product_data_5)

    assert exc_info.value.status_code == 400 and 'Negative price' in exc_info.value.detail

    product_update_data_3 = product_data_3
    product_update_data_3.category_id = 100
    with pytest.raises(HTTPException) as exc_info:
        await ProductService.update(test_session, 3, product_update_data_3)
    assert exc_info.value.status_code == 400 and 'Category not found' in exc_info.value.detail

    product_update_data_3.category_id = 2
    product_update_data_3.price = -2
    with pytest.raises(HTTPException) as exc_info:
        await ProductService.update(test_session, 3, product_update_data_3)
    assert exc_info.value.status_code == 400 and 'Negative price' in exc_info.value.detail

    product_update_data_3.price = 15.23
    product_update_data_3.title = product_data_2.title
    with pytest.raises(HTTPException) as exc_info:
        await ProductService.update(test_session, 3, product_update_data_3)
    assert exc_info.value.status_code == 400 and 'Duplicate produc' in exc_info.value.detail

    await ProductService.delete(test_session, 3)

    product_count = await test_session.execute(select(func.count()).select_from(Product))
    assert product_count.scalar() == 2

    # Products Characteristics
    characteristic_query_result = await test_session.execute(select(Characteristic))
    characteristics = characteristic_query_result.scalars().all()

    assert len(characteristics) == 3

    c1, c2, c3 = characteristics[0], characteristics[1], characteristics[2]

    assert c1.category_id == 1 and c2.category_id == 1 and c3.category_id != 1
    assert c1.id == 2 and c1.title == 'characteristic 2 cat 1' and c1.type == 'integer'
    assert c2.id == 3 and c2.title == 'characteristic 3 cat 1' and c2.type == 'string'
    assert c3.id == 6 and c3.title == 'characteristic 4' and c3.type == 'integer'

    with pytest.raises(HTTPException) as exc_info:
        await ProductService.add_characteristic(test_session, 1, [characteristic_value_type_err, ])
    assert 'Error data types, waiting integer' in exc_info.value.detail['messages']

    product = await ProductService.detail(test_session, 1, True)
    assert len(product.characteristics) == 0

    with pytest.raises(HTTPException) as exc_info:
        await ProductService.add_characteristic(test_session, 1, [characteristic_category_err, ])
    assert 'Characteristics do not belong to the products' in exc_info.value.detail

    # with pytest.raises(HTTPException) as exc_info:
    #     await ProductService.add_characteristic(test_session, 1, [characteristic_id_err, ])
    # assert 'A non-existent characteristic ID was passed.' in exc_info.value.detail

    ch_pr = await ProductService.add_characteristic(test_session, 1, [characteristic_1_c_1_product_1, ])
    assert len(ch_pr) == 1 and ch_pr[0].id == 1

    ch_pr = await ProductService.add_characteristic(test_session, 1, [characteristic_1_c_2_product_1, ])
    assert len(ch_pr) == 2

    # with pytest.raises(HTTPException) as exc_info:
    #     await ProductService.add_characteristic(test_session, 1, [characteristic_1_c_2_product_1, ])
    # assert 'Duplication characteristic' in exc_info.value.detail

    with pytest.raises(HTTPException) as exc_info:
        await ProductService.update_characteristic(
            test_session,
            product_id=1,
            data=[characteristic_update_type_err]
        )
    assert 'Error data types, waiting integer' in exc_info.value.detail['messages']

    await ProductService.update_characteristic(
        test_session,
        product_id=1,
        data=[characteristic_update]
    )

