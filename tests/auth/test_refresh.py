async def test_refresh_success(client, user_payload):
    register = await client.post('/users/', json=user_payload)
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
