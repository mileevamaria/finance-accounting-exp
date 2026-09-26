from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import UUIDMixin

if TYPE_CHECKING:
    from app.models import Company, Transaction


class Project(Base, UUIDMixin):
    __tablename__ = 'projects'

    __table_args__ = (
        Index('ix_projects_company', 'company_id'),
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey('companies.id', ondelete='CASCADE'),
    )
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(500))

    company: Mapped['Company'] = relationship(
        back_populates='projects',
    )

    transactions: Mapped[list['Transaction']] = relationship(
        back_populates='project',
    )
