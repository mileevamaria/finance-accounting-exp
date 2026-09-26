from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import SoftDeleteMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models import Account, Category, CategoryGroup, Project, User


class Company(Base, SoftDeleteMixin, UUIDMixin):
    __tablename__ = 'companies'

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
    )
    name: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None]
    inn: Mapped[str | None] = mapped_column(String(12), unique=True)
    kpp: Mapped[str | None] = mapped_column(String(9), unique=True)
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(20))
    address: Mapped[str | None] = mapped_column(String(255))

    owner: Mapped['User'] = relationship(
        back_populates='companies',
    )

    accounts: Mapped[list['Account']] = relationship(
        back_populates='company',
        cascade='all, delete-orphan',
    )

    category_groups: Mapped[list['CategoryGroup']] = relationship(
        back_populates='company',
        cascade='all, delete-orphan',
    )

    categories: Mapped[list['Category']] = relationship(
        back_populates='company',
        cascade='all, delete-orphan',
    )

    projects: Mapped[list['Project']] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
    )
