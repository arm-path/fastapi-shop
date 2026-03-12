import pytest
from fastapi import HTTPException
from sqlalchemy import select, update

from app.tests.data_user import (
    user_data_1,
    user_data_2,
    user_data_3,
    user_data_4, auth_data_1, auth_data_2, auth_data_3, auth_data_4
)
from app.user import User
from app.user.schemas import Token
from app.user.services import AuthUserService, password_verify, get_current_user


@pytest.mark.asyncio
async def test_create_user(test_session):
    await AuthUserService.registration(test_session, user_data_1)
    await AuthUserService.registration(test_session, user_data_2)
    await AuthUserService.registration(test_session, user_data_3)

    user_query_1 = await test_session.execute(select(User).where(User.id == 1))
    user_query_2 = await test_session.execute(select(User).where(User.id == 2))
    user_1 = user_query_1.scalar_one_or_none()
    user_2 = user_query_2.scalar_one_or_none()

    assert user_1.role == 'installer' and user_1.email == 'arm@example.com'
    assert user_2.role != 'installer'
    assert password_verify('123456$Py', user_1.password)

    try:
        await AuthUserService.registration(test_session, user_data_4)
    except HTTPException as e:
        assert '400: Email already exist.' in str(e)


@pytest.mark.asyncio
async def test_authentication_user(test_session):
    user_result_1 = await test_session.execute(select(User).where(User.id == 1))
    user_1 = user_result_1.scalar_one_or_none()
    assert user_1.id == 1

    user_result_2 = await test_session.execute(select(User).where(User.id == 2))
    user_2 = user_result_2.scalar_one_or_none()
    assert user_2.id == 2

    auth_token_1 = await AuthUserService.authentication(test_session, auth_data_1)
    assert type(auth_token_1) == Token

    auth_token_2 = await AuthUserService.authentication(test_session, auth_data_4)
    assert type(auth_token_2) == Token

    user_obj_1 = await get_current_user(auth_token_1.access_token, test_session)
    assert user_obj_1.id == user_1.id

    try:
        await get_current_user(auth_token_2.access_token, test_session)
    except HTTPException as e:
        assert '401: Could not validate credentials'

    await test_session.execute(update(User).where(User.id == 2).values(is_active=True))
    await test_session.commit()

    user_obj_2 = await get_current_user(auth_token_2.access_token, test_session)
    assert user_obj_2.id == user_2.id

    try:
        await get_current_user('Could not validate credentials', test_session)
    except HTTPException as e:
        assert '401: Could not validate credentials'

    try:
        await AuthUserService.authentication(test_session, auth_data_2)
    except HTTPException as e:
        assert '403: User or Password incorrect.' in str(e)

    try:
        await AuthUserService.authentication(test_session, auth_data_3)
    except HTTPException as e:
        assert '404: User not found.' in str(e)
