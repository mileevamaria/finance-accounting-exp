async def test_login_success(client):
    await client.post(
        '/users/',
        json={
            'first_name': 'John',
            'last_name': 'Dow',
            'email': 'john@test.com',
            'password': 'Password123',
        },
    )
    response = await client.post(
        '/auth/login',
        json={
            'identifier': 'john@test.com',
            'password': 'Password123',
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body['access_token']
    assert body['refresh_token']


async def test_login_wrong_password(client):
    await client.post(
        '/users/',
        json={
            'first_name': 'John',
            'last_name': 'Dow',
            'email': 'john@test.com',
            'password': 'Password123',
        },
    )
    response = await client.post(
        '/auth/login',
        json={
            'identifier': 'john@test.com',
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
