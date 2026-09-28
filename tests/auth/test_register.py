async def test_register_success(client, user_payload):
    response = await client.post(
        '/users/', 
        json={
            **user_payload,
            'email': 'john@example.com',
        },
    )
    assert response.status_code == 200, response.json()
    body = response.json()
    assert body['access_token']
    assert body['refresh_token']
    assert body['user']['email'] == 'john@example.com'


async def test_register_duplicate_email(client, user_payload, registered_user):
    response = await client.post('/users/', json=user_payload)
    assert response.status_code == 409
