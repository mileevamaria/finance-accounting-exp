async def test_get_me(client):
    register = await client.post(
        '/users/',
        json={
            'first_name': 'John',
            'last_name': 'Dow',
            'email': 'john@test.com',
            'password': 'Password123',
        },
    )
    token = register.json()['access_token']
    response = await client.get(
        '/users/me',
        headers={
            'Authorization': f'Bearer {token}',
        },
    )
    assert response.status_code == 200
    assert response.json()['email'] == 'john@test.com'
