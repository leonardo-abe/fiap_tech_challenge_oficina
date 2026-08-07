import os

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import app.infrastructure.persistence  # noqa: F401 - registra os models em Base.metadata
from app.infrastructure.db.session import Base

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://oficina_test:oficina_test@localhost:5433/oficina_test",
)


@pytest.fixture(scope="session")
async def engine():
    test_engine = create_async_engine(TEST_DATABASE_URL)
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield test_engine

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture
async def session(engine) -> AsyncSession:
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as db_session:
        yield db_session

    async with engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            await connection.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE')
            )
