from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.auth import Token
from app.models.mixins import SoftDeleteMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.companies import Company


class User(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'users'

    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(
        String(20), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_superuser: Mapped[bool] = mapped_column(default=False)

    refresh_tokens: Mapped[list[Token]] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )

    companies: Mapped[list["Company"]] = relationship(
        back_populates='owner',
        cascade='all, delete-orphan',
    )
