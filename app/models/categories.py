from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import UUIDMixin

if TYPE_CHECKING:
    from app.models import Company, Transaction


class CategoryGroup(Base, UUIDMixin):
    __tablename__ = 'category_groups'

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey('companies.id', ondelete='CASCADE'),
    )
    name: Mapped[str] = mapped_column(String(255))

    company: Mapped['Company'] = relationship(
        back_populates='category_groups',
    )

    categories: Mapped[list['Category']] = relationship(
        back_populates='group',
        cascade='all, delete-orphan',
    )


class CategoryIconColor(StrEnum):
    RED = '#F44336'
    PINK = '#E91E63'
    PURPLE = '#9C27B0'
    INDIGO = '#3F51B5'
    GREEN = '#4CAF50'
    LIGHT_BLUE = '#03A9F4'
    BLUE = '#2980B9'
    YELLOW = '#FFEB3B'
    ORANGE = '#FF9800'
    BLACK = '#000000'
    GREY = '#9E9E9E'
    BROWN = '#795548'
    WHITE = '#F5F5F5'


class Category(Base, UUIDMixin):
    __tablename__ = 'categories'

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey('companies.id', ondelete='CASCADE')
    )
    group_id: Mapped[UUID] = mapped_column(
        ForeignKey('category_groups.id', ondelete='CASCADE')
    )
    name: Mapped[str] = mapped_column(String(255))
    icon_color: Mapped[CategoryIconColor] = mapped_column(
        SQLEnum(CategoryIconColor),
        default=CategoryIconColor.GREY,
    )

    group: Mapped['CategoryGroup'] = relationship(
        back_populates='categories',
    )

    transactions: Mapped[list['Transaction']] = relationship(
        back_populates='category',
    )

    company: Mapped["Company"] = relationship(
        back_populates="categories",
    )
