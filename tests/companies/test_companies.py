async def test_create_company(client, auth_headers):
    response = await client.post(
        '/companies',
        headers=auth_headers,
        json={
            'name': 'My Company',
        },
    )
    print(response.text)
    assert response.status_code == 200, response.json()
    body = response.json()
    assert body['name'] == 'My Company'
    assert 'id' in body


async def test_get_company(client, auth_headers, company):
    response = await client.get(
        f"/companies/{company['id']}",
        headers=auth_headers,
    )
    assert response.status_code == 200, response.json()
    assert response.json()['id'] == company['id']


async def test_update_company(client, auth_headers, company):
    response = await client.patch(
        f"/companies/{company['id']}",
        headers=auth_headers,
        json={
            'name': 'Updated Company',
        },
    )
    assert response.status_code == 200, response.json()
    assert response.json()['name'] == 'Updated Company'


async def test_delete_company(client, auth_headers, company):
    response = await client.delete(
        f"/companies/{company['id']}",
        headers=auth_headers,
    )
    assert response.status_code == 204
    response = await client.get(
        f"/companies/{company['id']}",
        headers=auth_headers,
    )
    assert response.status_code == 404


async def test_cannot_access_foreign_company(client, company, foreign_user_payload):
    register = await client.post(
        '/users/',
        json=foreign_user_payload,
    )
    headers = {
        'Authorization': f'Bearer {register.json()['access_token']}'
    }
    response = await client.get(
        f"/companies/{company['id']}",
        headers=headers,
    )
    assert response.status_code == 404
