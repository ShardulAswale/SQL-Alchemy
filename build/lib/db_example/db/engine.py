import os
from functools import lru_cache

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.engine.url import URL

# Load environment variables from .env file (if present)
load_dotenv()


def _get_db_settings() -> dict:
    """Read DB settings from env with sensible defaults."""
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASS", "password"),
        "database": os.getenv("DB_NAME", "db_example"),
    }


@lru_cache(maxsize=1)
def get_async_engine() -> AsyncEngine:
    """Create and cache a single AsyncEngine instance."""
    settings = _get_db_settings()

    url = URL.create(
        drivername="mysql+asyncmy",
        username=settings["user"],
        password=settings["password"],
        host=settings["host"],
        port=settings["port"],
        database=settings["database"],
    )

    engine = create_async_engine(
        url,
        echo=False,
        future=True,
        pool_pre_ping=True,
    )
    return engine


# Async session factory used by UoW
async_session_factory = async_sessionmaker(
    bind=get_async_engine(),
    expire_on_commit=False,
    class_=AsyncSession,
)
