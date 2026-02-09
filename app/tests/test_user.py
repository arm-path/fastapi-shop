import pytest

from app.settings.database import test_async_session
from app.tests import Base


async def init_tables():
    async with test_async_session() as session:
        connection = await session.connection()
        await connection.run_sync(Base.metadata.drop_all)

        await connection.run_sync(Base.metadata.create_all)
        await session.commit()


@pytest.mark.asyncio
async def test_create_user():
    await init_tables()
