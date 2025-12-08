from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.settings.settings import settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(settings.postgres_url, echo=False)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


SessionDepends = Annotated[AsyncSession, Depends(get_session)]
