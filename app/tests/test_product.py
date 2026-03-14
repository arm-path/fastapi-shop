import pytest
from fastapi import HTTPException
from sqlalchemy import select

from app.product import Category
from app.product.services import CategoryService
from app.tests.data_product import (
    category_data_1, category_data_2, category_data_3, category_data_4, category_data_5, category_data_update

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
    assert len(categories) == 2 # With parent_id == None