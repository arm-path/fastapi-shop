import functools

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.settings.database import Base
from app.settings.settings import settings
from app.settings.triggers import (update_supplies_product_fn,
                                   update_supplies_draft_fn,
                                   update_order_is_active_fn,
                                   supplies_product_insert_tg,
                                   supplies_product_update_tg,
                                   supplies_product_delete_tg,
                                   update_supplies_draft_tg,
                                   update_order_is_active_tg)


async def init_tables(session: AsyncSession):
    connection = await session.connection()
    await connection.run_sync(Base.metadata.drop_all)

    await connection.run_sync(Base.metadata.create_all)
    await registration_triggers(session)
    await session.commit()


async def registration_triggers(session: AsyncSession):
    await session.execute(next(update_supplies_product_fn.to_sql_statement_create_or_replace()))
    await session.execute(next(update_supplies_draft_fn.to_sql_statement_create_or_replace()))
    await session.execute(next(update_order_is_active_fn.to_sql_statement_create_or_replace()))

    await session.execute(supplies_product_insert_tg.to_sql_statement_create())
    await session.execute(supplies_product_update_tg.to_sql_statement_create())
    await session.execute(supplies_product_delete_tg.to_sql_statement_create())
    await session.execute(update_supplies_draft_tg.to_sql_statement_create())
    await session.execute(update_order_is_active_tg.to_sql_statement_create())


def get_async_session_maker(database_url: str):
    async_engine = create_async_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )
    return async_sessionmaker(async_engine, expire_on_commit=False)


async def close_engine(session_maker):
    if session_maker.kw.get('bind'):
        await session_maker.kw['bind'].dispose()


@pytest.fixture(scope='session')
async def initialize_database():
    session_maker = get_async_session_maker(settings.test_postgres_url)
    async with session_maker() as session:
        try:
            await init_tables(session)
            yield
        finally:
            await session.close()
            await close_engine(session_maker)


@pytest.fixture
async def test_session(initialize_database):
    session_maker = get_async_session_maker(settings.test_postgres_url)
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
            await close_engine(session_maker)


async def error_session(func):
    session_maker = get_async_session_maker(settings.test_postgres_url)
    async with session_maker() as session:
        try:
            await func(session)
        finally:
            await session.close()
            await close_engine(session_maker)

async def assert_http_exception(func, expected_message: str):
    session_maker = get_async_session_maker(settings.test_postgres_url)
    async with session_maker() as session:
        new_func = functools.partial(
            func.func,
            session,
            *func.args[1:]
        )
        with pytest.raises(HTTPException) as exc_info:
            await new_func()
        assert expected_message in exc_info.value.detail
        await session.close()
        await close_engine(session_maker)