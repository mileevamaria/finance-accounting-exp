from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from yookassa import Payment

from app.core.config import settings
from app.models import Subscription
from app.models.subscriptions import (
    SubscriptionPlan,
    SubscriptionStatus,
)
from app.repositories import SubscriptionRepository
from app.schemas.subscriptions import (
    PaymentCreateResponse,
    SubscriptionResponse,
    YooKassaWebhook,
)


class SubscriptionService:
    def __init__(
        self,
        session: AsyncSession,
        subscription_repo: SubscriptionRepository,
    ):
        self.session = session
        self.subscription_repo = subscription_repo

    async def create_payment(self, user_id: UUID) -> PaymentCreateResponse:
        payment = Payment.create(
            {
                'amount': {
                    'value': settings.subscribtion_price,
                    'currency': settings.subscribtion_currency,
                },
                'capture': True,
                'confirmation': {
                    'type': 'redirect',
                    'return_url': settings.yookassa_return_url,
                },
                'description': settings.subscribtion_desc,
                'metadata': {
                    'user_id': str(user_id),
                    'plan': SubscriptionPlan.PRO.value,
                },
            },
            uuid4().hex,
        )

        return PaymentCreateResponse(
            payment_id=payment.id or '',
            confirmation_url=payment.confirmation.confirmation_url \
                if payment.confirmation else '',
        )

    async def process_webhook(self, event: YooKassaWebhook) -> None:
        if event.event != 'payment.succeeded':
            return

        payment_id = event.object.id

        async with self.session.begin():
            if await self.subscription_repo.exists_payment(payment_id):
                return
            user_id = UUID(event.object.metadata['user_id'])
            subscription = (
                await self.subscription_repo.get_by_user_for_update(user_id)
            )
            period_end = datetime.now(UTC) + timedelta(days=30)
            if subscription is None:
                await self.subscription_repo.create(
                    Subscription(
                        user_id=user_id,
                        provider_payment_id=payment_id,
                        plan=SubscriptionPlan.PRO,
                        status=SubscriptionStatus.ACTIVE,
                        current_period_end=period_end,
                    )
                )
                return

            subscription.provider_payment_id = payment_id
            subscription.plan = SubscriptionPlan.PRO
            subscription.status = SubscriptionStatus.ACTIVE
            subscription.current_period_end = period_end
            await self.subscription_repo.update(subscription)

    async def get_subscription(
        self,
        user_id: UUID,
    ) -> SubscriptionResponse:
        subscription = await self.subscription_repo.get_by_user(
            user_id,
        )
        if subscription is None:
            return SubscriptionResponse(
                plan=SubscriptionPlan.FREE,
                status=SubscriptionStatus.EXPIRED,
                current_period_end=None,
            )

        status: SubscriptionStatus | str = subscription.status

        if (
            subscription.status == SubscriptionStatus.ACTIVE
            and subscription.current_period_end is not None
            and subscription.current_period_end <= datetime.now(UTC)
        ):
            status = SubscriptionStatus.EXPIRED

        return SubscriptionResponse(
            plan=subscription.plan,
            status=status,
            current_period_end=subscription.current_period_end,
        )
