from sqlalchemy import UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, Boolean
from src.utils.constants import OnboardingStatusEnum

from src.db.base import Base

class UserModel(Base):
    """Model for demo purpose."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    externalId: Mapped[str] = mapped_column(String(length=200), nullable=True)
    name: Mapped[str] = mapped_column(String(length=200), nullable=True)
    email: Mapped[str] = mapped_column(String(length=200), nullable=True)
    onboardingStatus: Mapped[OnboardingStatusEnum] = mapped_column(
        Enum(OnboardingStatusEnum), nullable=True, default=OnboardingStatusEnum.NEW
    )

    __table_args__ = (UniqueConstraint("externalId"),)
