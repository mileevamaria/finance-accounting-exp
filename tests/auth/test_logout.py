async def test_logout_success(client, user_payload):
    register = await client.post('/users/', json=user_payload)
    refresh = register.json()['refresh_token']
    response = await client.post(
        '/auth/logout',
        json={
            'refresh_token': refresh,
        },
    )
    assert response.status_code == 204
