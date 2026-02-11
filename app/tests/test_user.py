import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings.database import test_async_session
from app.settings.triggers import update_supplies_product_fn, update_supplies_draft_fn, update_order_is_active_fn, \
    supplies_product_insert_tg, supplies_product_update_tg, supplies_product_delete_tg, update_supplies_draft_tg, \
    update_order_is_active_tg
from app.tests import Base


async def init_tables():
    async with test_async_session() as session:
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


@pytest.mark.asyncio
async def test_create_user():
    await init_tables()

