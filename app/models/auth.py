from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import UUIDMixin

if TYPE_CHECKING:
    from app.models.users import User


class Token(Base, UUIDMixin):
    __tablename__ = 'tokens'

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    token_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
)   
    expires_at: Mapped[datetime]
    revoked_at: Mapped[datetime | None]

    user: Mapped['User'] = relationship(
        back_populates='refresh_tokens'
    )
