async def test_register_success(client):
    response = await client.post(
        '/users/',
        json={
            'first_name': 'John',
            'last_name': 'Dow',
            'email': 'john@test.com',
            'password': 'Password123',
        },
    )
    assert response.status_code == 200, response.json()
    body = response.json()
    assert body['access_token']
    assert body['refresh_token']
    assert body['user']['email'] == 'john@test.com'


async def test_register_duplicate_email(client):
    payload = {
        'first_name': 'John',
        'last_name': 'Dow',
        'email': 'john@test.com',
        'password': 'Password123',
    }
    await client.post('/users/', json=payload)
    response = await client.post('/users/', json=payload)
    assert response.status_code == 409
