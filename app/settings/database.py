from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from app.settings.settings import settings
from app.utils import camel_to_snake


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)

    metadata = MetaData(naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_`%(constraint_name)s`',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s'
    })

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)


async_engine = create_async_engine(settings.postgres_url, echo=False)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

test_async_engine = create_async_engine(settings.test_postgres_url, echo=False)
test_async_session = async_sessionmaker(test_async_engine,expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


SessionDepends = Annotated[AsyncSession, Depends(get_session)]
