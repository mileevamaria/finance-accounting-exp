async def test_create_category_group(
    client,
    auth_headers,
    company,
):
    response = await client.post(
        f'/companies/{company["id"]}/category-groups',
        headers=auth_headers,
        json={
            'name': 'Доходы',
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['company_id'] == company['id']
    assert data['name'] == 'Доходы'


async def test_get_category_groups(
    client,
    auth_headers,
    company,
    category_group,
):
    response = await client.get(
        f'/companies/{company["id"]}/category-groups',
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert len(data) == 1
    assert data[0]['id'] == category_group['id']
    assert data[0]['name'] == 'Доходы'


async def test_get_category_group(
    client,
    auth_headers,
    company,
    category_group,
):
    response = await client.get(
        f'/companies/{company["id"]}/category-groups/{category_group["id"]}',
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['id'] == category_group['id']
    assert data['company_id'] == company['id']
    assert data['name'] == 'Доходы'


async def test_update_category_group(
    client,
    auth_headers,
    company,
    category_group,
):
    response = await client.patch(
        f'/companies/{company["id"]}/category-groups/{category_group["id"]}',
        headers=auth_headers,
        json={'name': 'Расходы'},
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['id'] == category_group['id']
    assert data['name'] == 'Расходы'


async def test_delete_category_group(
    client,
    auth_headers,
    company,
    category_group,
):
    endpoint = (
        f'/companies/{company["id"]}/category-groups/'
        f'{category_group["id"]}'
    )
    response = await client.delete(endpoint, headers=auth_headers)
    assert response.status_code == 204

    response = await client.get(endpoint, headers=auth_headers)
    assert response.status_code == 404


async def test_cannot_access_foreign_category_group(
    client,
    company,
    category_group,
    foreign_auth_headers,
):
    response = await client.get(
        f'/companies/{company["id"]}/category-groups/{category_group["id"]}',
        headers=foreign_auth_headers,
    )
    assert response.status_code == 404
