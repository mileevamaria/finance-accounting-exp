async def test_create_account(client, auth_headers, company):
    response = await client.post(
        f'/companies/{company["id"]}/accounts',
        headers=auth_headers,
        json={
            'name': 'Main account',
            'type': 'bank',
            'currency': 'rub',
            'opening_balance': '1000.00',
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data['company_id'] == company["id"]
    assert data['name'] == 'Main account'
    assert data['type'] == 'bank'
    assert data['currency'] == 'rub'
    assert data['opening_balance'] == '1000.00'


async def test_get_accounts(
    client,
    auth_headers,
    company,
    account,
):
    response = await client.get(
        f'/companies/{company["id"]}/accounts',
        headers=auth_headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == account["id"]
    assert data[0]['company_id'] == company["id"]


async def test_get_account(
    client,
    auth_headers,
    company,
    account,
):
    response = await client.get(
        f'/companies/{company["id"]}/accounts/{account["id"]}',
        headers=auth_headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == account["id"]
    assert data['company_id'] == company["id"]
    assert data['name'] == 'Main account'
    assert data['currency'] == 'rub'


async def test_update_account(
    client,
    auth_headers,
    company,
    account,
):
    response = await client.patch(
        f'/companies/{company["id"]}/accounts/{account["id"]}',
        headers=auth_headers,
        json={
            'name': 'Новый счёт',
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == account["id"]
    assert data['name'] == 'Новый счёт'


async def test_delete_account(
    client,
    auth_headers,
    company,
    account,
):
    response = await client.delete(
        f'/companies/{company["id"]}/accounts/{account["id"]}',
        headers=auth_headers,
    )

    assert response.status_code == 204

    response = await client.get(
        f'/companies/{company["id"]}/accounts/{account["id"]}',
        headers=auth_headers,
    )

    assert response.status_code == 404


async def test_cannot_access_foreign_account(
    client,
    company,
    account,
    foreign_auth_headers,
):
    response = await client.get(
        f'/companies/{company["id"]}/accounts/{account["id"]}',
        headers=foreign_auth_headers,
    )

    assert response.status_code == 404


async def test_cannot_create_account_in_foreign_company(
    client,
    company,
    foreign_auth_headers,
):
    response = await client.post(
        f'/companies/{company["id"]}/accounts',
        headers=foreign_auth_headers,
        json={
            'name': 'Чужой счёт',
            'type': 'bank',
            'currency': 'rub',
            'opening_balance': '1000.00',
        },
    )

    assert response.status_code == 404
