from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy import select

from app.models.subscriptions import (
    Subscription,
    SubscriptionPlan,
    SubscriptionStatus,
)


async def test_get_subscription_without_subscription(
    client,
    auth_headers,
):
    response = await client.get('/subscription/get', headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['plan'] == 'free'
    assert data['status'] == 'expired'
    assert data['current_period_end'] is None


async def test_create_payment(
    client,
    auth_headers,
    monkeypatch,
):
    class FakeConfirmation:
        confirmation_url = 'https://example.com/payment'

    class FakePayment:
        id = 'payment-123'
        confirmation = FakeConfirmation()

    def fake_create(*args, **kwargs):
        return FakePayment()

    monkeypatch.setattr(
        'app.services.subscriptions.Payment.create',
        fake_create,
    )

    response = await client.post('/subscription/payment', headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['payment_id'] == 'payment-123'
    assert data['confirmation_url'] == 'https://example.com/payment'


async def test_process_webhook_creates_subscription(
    client,
    session,
    registered_user,
):
    await session.commit()
    event = {
        'event': 'payment.succeeded',
        'object': {
            'id': 'payment-123',
            'metadata': {
                'user_id': registered_user['user']['id'],
                'plan': 'pro',
            },
        },
    }

    response = await client.post('/subscription/webhook', json=event)
    assert response.status_code == 204

    result = await session.execute(
        select(Subscription).where(
            Subscription.user_id == registered_user['user']['id'],
        )
    )
    subscription = result.scalar_one()
    assert subscription.provider_payment_id == 'payment-123'
    assert subscription.plan == SubscriptionPlan.PRO
    assert subscription.status == SubscriptionStatus.ACTIVE
    assert subscription.current_period_end is not None


async def test_duplicate_webhook_is_ignored(
    client,
    session,
    registered_user,
):
    await session.commit()
    event_id = str(uuid4())
    event = {
        'event': 'payment.succeeded',
        'object': {
            'id': event_id,
            'metadata': {
                'user_id': registered_user['user']['id'],
                'plan': 'pro',
            },
        },
    }

    response = await client.post('/subscription/webhook', json=event)
    assert response.status_code == 204

    response = await client.post('/subscription/webhook', json=event)
    assert response.status_code == 204

    result = await session.execute(
        select(Subscription).where(
            Subscription.user_id == registered_user['user']['id'],
        )
    )
    subscriptions = result.scalars().all()
    assert len(subscriptions) == 1


async def test_process_webhook_updates_existing_subscription(
    client,
    session,
    subscription,
    registered_user,
):
    old_payment_id = subscription.provider_payment_id

    event = {
        'event': 'payment.succeeded',
        'object': {
            'id': 'new-payment',
            'metadata': {
                'user_id': registered_user['user']['id'],
                'plan': 'pro',
            },
        },
    }

    response = await client.post('/subscription/webhook', json=event)
    assert response.status_code == 204

    await session.refresh(subscription)
    assert subscription.provider_payment_id != old_payment_id
    assert subscription.provider_payment_id == 'new-payment'
    assert subscription.plan == SubscriptionPlan.PRO
    assert subscription.status == SubscriptionStatus.ACTIVE
    assert subscription.current_period_end is not None
    assert subscription.current_period_end > datetime.now(UTC)


async def test_webhook_ignores_other_events(
    client,
    session,
    registered_user,
):
    event = {
        'event': 'payment.canceled',
        'object': {
            'id': 'payment-123',
            'metadata': {
                'user_id': registered_user['user']['id'],
                'plan': 'pro',
            },
        },
    }

    response = await client.post('/subscription/webhook', json=event)
    assert response.status_code == 204

    result = await session.execute(
        select(Subscription).where(
            Subscription.user_id == registered_user['user']['id'],
        )
    )
    assert result.scalar_one_or_none() is None


async def test_get_active_subscription(client, auth_headers, subscription):
    response = await client.get('/subscription/get', headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['plan'] == 'pro'
    assert data['status'] == 'active'
    assert data['current_period_end'] is not None


async def test_get_subscription_returns_expired_when_period_has_ended(
    client,
    session,
    subscription,
    auth_headers,
):
    subscription.current_period_end = (
        datetime.now(UTC) - timedelta(days=1)
    )
    await session.commit()

    response = await client.get('/subscription/get', headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['plan'] == 'pro'
    assert data['status'] == 'expired'
    assert data['current_period_end'] is not None


async def test_get_subscription_requires_auth(client):
    response = await client.get('/subscription/get')
    assert response.status_code == 401


async def test_create_payment_requires_auth(client):
    response = await client.post('/subscription/payment')
    assert response.status_code == 401
