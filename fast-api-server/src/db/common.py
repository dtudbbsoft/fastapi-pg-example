from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

from src.settings import settings


async def create_database() -> None:
    """Create a database."""
    db_url = make_url(str(settings.db_url.with_path("/postgres")))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        database_existance = await conn.execute(
            text("SELECT * FROM users WHERE datname=:db_name"),
            {"db_name": settings.db_base}
        )
        database_exists = database_existance.scalar() == 1

    if database_exists:
        await drop_database()

    async with engine.connect() as conn:
        await conn.execute(
            text(
                'CREATE DATABASE :db_name ENCODING "utf8" TEMPLATE template1',  # noqa: E501
            ),
            {"db_name": settings.db_base}
        )


async def drop_database() -> None:
    """Drop current database."""
    db_url = make_url(str(settings.db_url.with_path("/postgres")))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        disc_users = (
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "  # noqa: S608
            "FROM pg_stat_activity "
            "WHERE pg_stat_activity.datname = :db_name "
            "AND pid <> pg_backend_pid();"
        )
        await conn.execute(text(disc_users), {"db_name": settings.db_base})
        await conn.execute(text("DROP DATABASE :db_name"), {"db_name": settings.db_base})
