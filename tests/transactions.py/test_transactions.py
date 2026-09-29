async def test_create_transaction(
    client,
    auth_headers,
    company,
    account,
    category,
):
    response = await client.post(
        f'/companies/{company["id"]}/accounts/{account["id"]}/transactions',
        headers=auth_headers,
        json={
            'amount': '500.00',
            'category_id': category["id"],
            'occurred_at': '2026-09-28T12:00:00Z',
            'counterparty': 'ООО Ромашка',
            'description': 'Оплата услуг',
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['account_id'] == account["id"]
    assert data['category_id'] == category["id"]
    assert data['amount'] == '500.00'
    assert data['counterparty'] == 'ООО Ромашка'
    assert data['description'] == 'Оплата услуг'


async def test_get_transactions(
    client,
    auth_headers,
    company,
    account,
    transaction,
):
    response = await client.get(
        f'/companies/{company["id"]}/accounts/{account["id"]}/transactions',
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert len(data) == 1
    assert data[0]['id'] == transaction['id']


async def test_get_transaction(
    client,
    auth_headers,
    company,
    account,
    transaction,
):
    endpoint = (
        f'/companies/{company["id"]}/accounts/{account["id"]}/'
        f'transactions/{transaction["id"]}'
    )
    response = await client.get(endpoint, headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["id"] == transaction["id"]
    assert data['account_id'] == account["id"]
    assert data['category_id'] == transaction['category_id']


async def test_update_transaction(
    client,
    auth_headers,
    company,
    account,
    transaction,
):
    endpoint = (
        f'/companies/{company["id"]}/accounts/{account["id"]}/'
        f'transactions/{transaction["id"]}'
    )
    response = await client.patch(
        endpoint,
        headers=auth_headers,
        json={
            'amount': '750.00',
            'description': 'Изменённое описание',
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['id'] == transaction['id']
    assert data['amount'] == '750.00'
    assert data['description'] == 'Изменённое описание'


async def test_delete_transaction(
    client,
    auth_headers,
    company,
    account,
    transaction,
):
    endpoint = (
        f'/companies/{company["id"]}/accounts/{account["id"]}/'
        f'transactions/{transaction["id"]}'
    )
    response = await client.delete(endpoint, headers=auth_headers)
    assert response.status_code == 204

    response = await client.get(endpoint, headers=auth_headers)
    assert response.status_code == 404


async def test_cannot_access_foreign_transaction(
    client,
    company,
    account,
    transaction,
    foreign_auth_headers,
):
    endpoint = (
        f'/companies/{company["id"]}/accounts/{account["id"]}/'
        f'transactions/{transaction["id"]}'
    )
    response = await client.get(endpoint, headers=foreign_auth_headers)
    assert response.status_code == 404


async def test_cannot_create_transaction_with_foreign_category(
    client,
    auth_headers,
    company,
    account,
    foreign_category,
):
    response = await client.post(
        f'/companies/{company["id"]}/accounts/{account["id"]}/transactions',
        headers=auth_headers,
        json={
            'amount': '500.00',
            'category_id': foreign_category["id"],
            'occurred_at': '2026-09-28T12:00:00Z',
        },
    )
    assert response.status_code == 404


async def test_cannot_create_transaction_in_foreign_account(
    client,
    company,
    foreign_account,
    category,
    auth_headers,
):
    response = await client.post(
        f'/companies/{company["id"]}/accounts/{foreign_account["id"]}/transactions',
        headers=auth_headers,
        json={
            'amount': '500.00',
            'category_id': category["id"],
            'occurred_at': '2026-09-28T12:00:00Z',
        },
    )
    assert response.status_code == 404
