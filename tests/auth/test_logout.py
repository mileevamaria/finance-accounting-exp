async def test_logout_success(client):
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
        '/auth/logout',
        json={
            'refresh_token': refresh,
        },
    )
    assert response.status_code == 204
