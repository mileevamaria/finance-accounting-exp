async def test_create_category(
    client,
    auth_headers,
    company,
    category_group,
):
    response = await client.post(
        f'/companies/{company["id"]}/categories',
        headers=auth_headers,
        json={
            'group_id': category_group['id'],
            'name': 'Зарплата',
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['company_id'] == company['id']
    assert data['group_id'] == category_group['id']
    assert data['name'] == 'Зарплата'
    assert data['icon_color'] == '#9E9E9E'


async def test_get_categories(
    client,
    auth_headers,
    company,
    category,
):
    response = await client.get(
        f'/companies/{company["id"]}/categories',
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert len(data) == 1
    assert data[0]['id'] == category['id']
    assert data[0]['name'] == 'Зарплата'


async def test_get_category(
    client,
    auth_headers,
    company,
    category,
):
    response = await client.get(
        f'/companies/{company["id"]}/categories/{category["id"]}',
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['id'] == category['id']
    assert data['company_id'] == company['id']
    assert data['group_id'] == category['group_id']
    assert data['name'] == 'Зарплата'


async def test_update_category(
    client,
    auth_headers,
    company,
    category,
):
    response = await client.patch(
        f'/companies/{company["id"]}/categories/{category["id"]}',
        headers=auth_headers,
        json={
            'name': 'Новая категория',
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['id'] == category['id']
    assert data['name'] == 'Новая категория'


async def test_update_category_group(
    client,
    auth_headers,
    company,
    category,
    second_category_group,
):
    response = await client.patch(
        f'/companies/{company["id"]}/categories/{category["id"]}',
        headers=auth_headers,
        json={
            'group_id': second_category_group['id'],
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['id'] == category['id']
    assert data['group_id'] == second_category_group['id']


async def test_delete_category(
    client,
    auth_headers,
    company,
    category,
):
    endpoint = f'/companies/{company["id"]}/categories/{category["id"]}'
    response = await client.delete(endpoint, headers=auth_headers)
    assert response.status_code == 204

    response = await client.get(endpoint, headers=auth_headers)
    assert response.status_code == 404


async def test_cannot_access_foreign_category(
    client,
    company,
    category,
    foreign_auth_headers,
):
    response = await client.get(
        f'/companies/{company["id"]}/categories/{category["id"]}',
        headers=foreign_auth_headers,
    )
    assert response.status_code == 404


async def test_cannot_create_category_with_foreign_group(
    client,
    company,
    foreign_category_group,
    auth_headers,
):
    response = await client.post(
        f'/companies/{company["id"]}/categories',
        headers=auth_headers,
        json={
            'group_id': foreign_category_group['id'],
            'name': 'Чужая категория',
        },
    )
    assert response.status_code == 404
