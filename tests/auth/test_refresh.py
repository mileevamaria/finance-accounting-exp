async def test_refresh_success(client):
    register = await client.post(
        '/users/',
        json={
            'first_name': 'John',
            'last_name': 'Dow',
            'email': 'john@test.com',
            'password': 'Password123',
        },
    )
    refresh = register.json()['refresh_token']
    response = await client.post(
        '/auth/refresh',
        json={
            'refresh_token': refresh,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body['access_token']
    assert body['refresh_token'] != refresh
