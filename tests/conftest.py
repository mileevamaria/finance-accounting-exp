from collections.abc import AsyncGenerator
from uuid import uuid4

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.core import settings
from app.db import get_session
from app.db.base import Base
from app.main import app

engine = create_async_engine(
    settings.test_database_url,
    poolclass=NullPool,
)

TestingSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def prepare_database() -> AsyncGenerator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[AsyncSession]:
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client(session: AsyncSession):
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test',
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user_payload():
    return {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': f'{uuid4()}@example.com',
            'password': 'Password123',
    }


@pytest_asyncio.fixture
async def foreign_user_payload():
    return {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': f'{uuid4()}@example.com',
        'password': 'Password123',
    }


@pytest_asyncio.fixture
async def registered_user(client, user_payload):
    response = await client.post('/users/', json=user_payload)
    assert response.status_code == 200, response.json()
    return response.json()


@pytest_asyncio.fixture
async def registered_foreign_user(client, foreign_user_payload):
    response = await client.post('/users/', json=foreign_user_payload)
    assert response.status_code == 200, response.json()
    return response.json()
    

@pytest_asyncio.fixture
async def auth_headers(registered_user):
    token_header =  f'Bearer {registered_user['access_token']}'
    return {'Authorization': token_header}
    

@pytest_asyncio.fixture
async def foreign_auth_headers(registered_foreign_user):
    token_header = f'Bearer {registered_foreign_user['access_token']}'
    return {'Authorization': token_header}


@pytest_asyncio.fixture
async def company(client, auth_headers):
    response = await client.post(
        '/companies',
        headers=auth_headers,
        json={
            'name': 'Test Company',
        },
    )
    assert response.status_code == 200, response.json()
    return response.json()


@pytest_asyncio.fixture
async def foreign_company(client, foreign_auth_headers):
    response = await client.post(
        '/companies',
        headers=foreign_auth_headers,
        json={
            'name': 'Test Company 2',
        },
    )
    assert response.status_code == 200, response.json()
    return response.json()


@pytest_asyncio.fixture
async def account(client, auth_headers, company):
    response = await client.post(
        f'/companies/{company["id"]}/accounts',
        headers=auth_headers,
        json={
            'name': 'Main account',
            'currency': 'rub',
            'opening_balance': '1000.00',
        },
    )
    assert response.status_code == 200, response.json()
    return response.json()


@pytest_asyncio.fixture
async def foreign_account(client, foreign_auth_headers, foreign_company):
    response = await client.post(
        f'/companies/{foreign_company["id"]}/accounts',
        headers=foreign_auth_headers,
        json={
            'name': 'Main account 2',
            'currency': 'rub',
            'opening_balance': '2000.00',
        },
    )
    assert response.status_code == 200, response.json()
    return response.json()


@pytest_asyncio.fixture
async def category_group(client, auth_headers, company):
    response = await client.post(
        f'/companies/{company["id"]}/category-groups',
        headers=auth_headers,
        json={
            'name': 'Доходы',
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


@pytest_asyncio.fixture
async def second_category_group(client, auth_headers, company):
    response = await client.post(
        f'/companies/{company["id"]}/category-groups',
        headers=auth_headers,
        json={
            'name': 'Расходы',
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


@pytest_asyncio.fixture
async def foreign_category_group(
    client, 
    foreign_auth_headers, 
    foreign_company,
):
    response = await client.post(
        f'/companies/{foreign_company["id"]}/category-groups',
        headers=foreign_auth_headers,
        json={
            'name': 'Переводы',
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


@pytest_asyncio.fixture
async def category(client, auth_headers, company, category_group):
    response = await client.post(
        f'/companies/{company["id"]}/categories',
        headers=auth_headers,
        json={
            'group_id': category_group['id'],
            'name': 'Зарплата',
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


@pytest_asyncio.fixture
async def foreign_category(
    client, 
    foreign_auth_headers, 
    foreign_company, 
    foreign_category_group,
):
    response = await client.post(
        f'/companies/{foreign_company["id"]}/categories',
        headers=foreign_auth_headers,
        json={
            'group_id': foreign_category_group['id'],
            'name': 'Зарплата',
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


@pytest_asyncio.fixture
async def transaction(client, auth_headers, company, account, category):
    response = await client.post(
        f'/companies/{company["id"]}/accounts/{account["id"]}/transactions',
        headers=auth_headers,
        json={
            'amount': '500.00',
            'category_id': category['id'],
            'occurred_at': '2026-09-28T12:00:00Z',
            'counterparty': 'ООО Ромашка',
            'description': 'Оплата услуг',
        },
    )
    assert response.status_code == 200, response.text
    return response.json()
