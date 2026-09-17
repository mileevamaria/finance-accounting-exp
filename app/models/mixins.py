from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )


class UUIDMixin:
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )


class SoftDeleteMixin(UUIDMixin):
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)
