from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, Boolean, ARRAY

from src.db.base import Base

class FixtureModel(Base):
    """Model for demo purpose."""

    __tablename__ = "fixture"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    externalId: Mapped[str] = mapped_column(String(length=200), nullable=False)
    name: Mapped[str] = mapped_column(String(length=200), nullable=True)
    fixtureUrl: Mapped[str] = mapped_column(String(length=200), nullable=True)
    createdBy: Mapped[str] = mapped_column(String(length=200), nullable=True)
    createdDate: Mapped[str] = mapped_column(String(length=200), nullable=True)
    modifiedDate: Mapped[str] = mapped_column(String(length=200), nullable=True)
    demo: Mapped[bool] = mapped_column(Boolean(), nullable=True)
    statuses: Mapped[[str]] = mapped_column(
        ARRAY(String(length=200)), nullable=True
    )

    __table_args__ = (UniqueConstraint("externalId"),)
