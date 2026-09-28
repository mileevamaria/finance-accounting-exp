from fastapi import APIRouter, Response, status

from app.core.dependencies import (
    CurrentUserDep,
    SubscriptionServiceDep,
)
from app.schemas.subscriptions import (
    PaymentCreateResponse,
    SubscriptionResponse,
    YooKassaWebhook,
)

router = APIRouter(
    prefix='/subscription',
    tags=['Subscription'],
)


@router.post(
    '/payment',
    response_model=PaymentCreateResponse,
)
async def create_payment(
    current_user: CurrentUserDep,
    service: SubscriptionServiceDep,
):
    return await service.create_payment(current_user.id)


@router.post(
    '/webhook',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def webhook(
    event: YooKassaWebhook,
    service: SubscriptionServiceDep,
):
    await service.process_webhook(event)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '/get',
    response_model=SubscriptionResponse,
)
async def get_subscription(
    current_user: CurrentUserDep,
    service: SubscriptionServiceDep,
):
    return await service.get_subscription(current_user.id)
