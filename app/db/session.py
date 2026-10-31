import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

logger = logging.getLogger(__name__)

Base = declarative_base()

def _get_connect_args(url_str: str) -> dict:
    args = {
        "timeout": 15,
        "command_timeout": 30,
        "statement_cache_size": 0,
    }
    lower = url_str.lower()
    is_local = "localhost" in lower or "127.0.0.1" in lower or "@postgres:" in lower or "@db:" in lower
    if not is_local:
        # Remote managed databases (Supabase, Neon, Render, AWS) require SSL
        args["ssl"] = "require"
    return args


# Build async engine with smart SSL and connection pooling
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=5,
    connect_args=_get_connect_args(settings.DATABASE_URL),
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
