from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import Select, select, Result, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, lazyload

from app.settings.database import SessionDepends
from app.settings.settings import settings
from app.user.models import User
from app.user.schemas import RegistrationSchema, Token

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/authentication/')


def password_hashed(password: str) -> str:
    return password_hash.hash(password)


def password_verify(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    token: str = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDepends):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get('sub')
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user_query: Select = (
        select(User)
        .options(
            lazyload(User.cart),
            load_only(User.id, User.email, User.first_name, User.last_name, User.role)
        )
        .where(User.email == email, User.is_active == True)
    )
    user_result: Result = await session.execute(user_query)
    user: User = user_result.scalar_one_or_none()
    if not user:
        print(f'get_current_user: {email} - User not Found')
        raise credentials_exception
    return user


CurrentUserDepends = Annotated[User, Depends(get_current_user)]


async def get_installer_user(user: CurrentUserDepends):
    if user.role == 'installer':
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied.')


InstallerUserDepends = Annotated[User, Depends(get_installer_user)]


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
    async def authentication(cls, session: AsyncSession, data: OAuth2PasswordRequestForm) -> Token:
        user_query: Select = select(User).where(User.email == data.username)
        user_result: Result = await session.execute(user_query)
        user: User | None = user_result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail='User not found.')
        if not password_verify(data.password, user.password):
            raise HTTPException(status_code=403, detail='User or Password incorrect.')
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
        return Token(access_token=access_token, token_type='bearer')
