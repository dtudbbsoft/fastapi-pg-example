from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.db.meta import meta


class Base(AsyncAttrs, DeclarativeBase):
    """Base for all models."""

    metadata = meta
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), nullable=False
    )
    updatedAt: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), onupdate=func.now(), nullable=True
    )
