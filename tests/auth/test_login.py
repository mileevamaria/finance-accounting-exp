async def test_login_success(client, user_payload, registered_user):
    response = await client.post(
        '/auth/login',
        json={
            'identifier': user_payload['email'],
            'password': user_payload['password'],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body['access_token']
    assert body['refresh_token']


async def test_login_wrong_password(client, user_payload, registered_user):
    response = await client.post(
        '/auth/login',
        json={
            'identifier': user_payload['email'],
            'password': 'WrongPassword123',
        },
    )
    assert response.status_code == 401
    assert response.json()['detail'] == 'Invalid credentials'


async def test_login_unknown_user(client):
    response = await client.post(
        '/auth/login',
        json={
            'identifier': 'unknown@test.com',
            'password': 'Password123',
        },
    )
    assert response.status_code == 401
