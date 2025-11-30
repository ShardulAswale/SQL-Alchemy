import os
from typing import AsyncIterator

import pytest_asyncio
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from db_example.db.base import Base

TEST_DB_NAME = os.getenv("DB_NAME", "test_db_example")


@pytest_asyncio.fixture
async def test_engine() -> AsyncIterator[AsyncEngine]:
    """
    Async engine pointing to the test database.
    Function-scoped so it always uses the current test's event loop.
    """
    url = URL.create(
        drivername="mysql+asyncmy",
        username=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASS", "password123"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=TEST_DB_NAME,
    )

    engine = create_async_engine(
        url,
        echo=False,
        future=True,
        pool_pre_ping=True,
    )

    # Fresh schema for each test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    """
    AsyncSession per test. pytest-asyncio manages the event loop.
    """
    session_factory = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with session_factory() as session:
        yield session
        await session.rollback()
