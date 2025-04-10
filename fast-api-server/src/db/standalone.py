import contextlib

from fast_api_db.db import session_factory


@contextlib.asynccontextmanager
async def get_standalone_session():
    session = session_factory()
    try:
        yield session
    finally:
        await session.close()
        await session_factory.kw["bind"].dispose()
