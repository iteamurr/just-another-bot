from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def build_session_factory(*, dsn: str, pool_size: int = 10, max_overflow: int = 20) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(dsn, pool_size=pool_size, max_overflow=max_overflow)
    return async_sessionmaker(engine, expire_on_commit=False)


async def get_session(factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with factory() as session:
        yield session
