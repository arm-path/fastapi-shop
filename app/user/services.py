from fastapi import HTTPException
from pwdlib import PasswordHash
from sqlalchemy import Select, select, Result, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.models import User
from app.user.schemas import RegistrationSchema, AuthSchema

password_hash = PasswordHash.recommended()


def password_hashed(password: str) -> str:
    return password_hash.hash(password)


def password_verify(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


class AuthUserService:
    @classmethod
    async def registration(cls, session: AsyncSession, data: RegistrationSchema) -> None:
        user_count_query: Select = select(func.count()).select_from(User)
        user_count_result: Result = await session.execute(user_count_query)
        user_count: int = user_count_result.scalar()

        data_dict = data.__dict__
        data_dict.pop('password_repeat')
        data_dict['password'] = password_hashed(data.password)

        if user_count == 0:
            data_dict['role'] = 'installer'
            data_dict['is_active'] = True

        user = User(**data_dict)
        session.add(user)
        try:
            await session.commit()
        except IntegrityError as e:
            if e.orig.pgcode == '23505':
                raise HTTPException(status_code=400, detail='Email already exist.')

    @classmethod
    async def authentication(cls, session: AsyncSession, data: AuthSchema) -> User:
        user_query: Select = select(User).where(User.email == data.email)
        user_result: Result = await session.execute(user_query)
        user: User | None = user_result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail='User not found.')
        if not password_verify(data.password, user.password):
            raise HTTPException(status_code=403, detail='User or Password incorrect.')
        return user
