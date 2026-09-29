from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import UUIDMixin

if TYPE_CHECKING:
    from app.models import User


class SubscriptionPlan(StrEnum):
    FREE = 'free'
    PRO = 'pro'


class SubscriptionStatus(StrEnum):
    PENDING = 'pending'
    ACTIVE = 'active'
    CANCELED = 'canceled'
    EXPIRED = 'expired'


class Subscription(Base, UUIDMixin):
    __tablename__ = 'subscriptions'

    __table_args__ = (
        Index('ix_subscriptions_user', 'user_id'),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        unique=True,
    )
    provider_payment_id: Mapped[str | None] = mapped_column(
        String(255), unique=True, index=True,
    )
    plan: Mapped[SubscriptionPlan] = mapped_column(
        SAEnum(
            SubscriptionPlan,
            values_callable=lambda e: [i.value for i in e],
            name='subscription_plan',
        ),
        default=SubscriptionPlan.FREE,
    )
    status: Mapped[SubscriptionStatus] = mapped_column(
        SAEnum(
            SubscriptionStatus,
            values_callable=lambda e: [i.value for i in e],
            name='subscription_status',
        ),
        default=SubscriptionStatus.PENDING,
    )
    current_period_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    user: Mapped['User'] = relationship(back_populates='subscription')
