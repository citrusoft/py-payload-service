import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    # fallback to local sqlite for development
    DATABASE_URL = "sqlite+aiosqlite:///./dev_payloads.db"

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
