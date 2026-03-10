import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import select

from app.user import User
from app.user.schemas import RegistrationSchema
from app.user.services import AuthUserService, password_verify

user_data = [
    RegistrationSchema(
        email='arm@example.com',
        first_name='Rinat',
        last_name='Ahtyamov',
        password='123456$Py',
        password_repeat='123456$Py'
    ),
    RegistrationSchema(
        email='lorem@example.com',
        first_name='Lorem',
        last_name='Ipsum',
        password='123456$Py',
        password_repeat='123456$Py'
    ),
    RegistrationSchema(
        email='consectetur@example.ru',
        first_name='Consectetur',
        last_name='Adipiscing',
        password='123456$Py',
        password_repeat='123456$Py'
    ),
    RegistrationSchema(
        email='consectetur@example.ru',
        first_name='Consectetur',
        last_name='Adipiscing',
        password='123456$Py',
        password_repeat='123456$Py',
    ),
]


@pytest.mark.asyncio
async def test_create_user(test_session):

    await AuthUserService.registration(test_session, user_data[0])
    await AuthUserService.registration(test_session, user_data[1])
    await AuthUserService.registration(test_session, user_data[2])

    user_query_1 = await test_session.execute(select(User).where(User.id == 1))
    user_query_2 = await test_session.execute(select(User).where(User.id == 2))
    user_1 = user_query_1.scalar_one_or_none()
    user_2 = user_query_2.scalar_one_or_none()

    assert user_1.role == 'installer' and user_1.email == 'arm@example.com'
    assert user_2.role != 'installer'
    assert password_verify('123456$Py', user_1.password)

    try:
        await AuthUserService.registration(test_session, user_data[3])
    except HTTPException as e:
        print(e.detail)
        assert '400: Email already exist.' in str(e)
