async def test_create_project(
    client,
    auth_headers,
    company,
):
    response = await client.post(
        f'/companies/{company["id"]}/projects',
        headers=auth_headers,
        json={
            'name': 'Проект 1',
            'description': 'Описание проекта',
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['company_id'] == company['id']
    assert data['name'] == 'Проект 1'
    assert data['description'] == 'Описание проекта'


async def test_get_projects(
    client,
    auth_headers,
    company,
    project,
):
    response = await client.get(
        f'/companies/{company["id"]}/projects',
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert len(data) == 1
    assert data[0]['id'] == project['id']
    assert data[0]['company_id'] == company['id']
    assert data[0]['name'] == 'Проект 1'


async def test_get_project(
    client,
    auth_headers,
    company,
    project,
):
    response = await client.get(
        f'/companies/{company["id"]}/projects/{project["id"]}',
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['id'] == project['id']
    assert data['company_id'] == company['id']
    assert data['name'] == 'Проект 1'
    assert data['description'] == 'Описание проекта'


async def test_update_project(
    client,
    auth_headers,
    company,
    project,
):
    response = await client.patch(
        f'/companies/{company["id"]}/projects/{project["id"]}',
        headers=auth_headers,
        json={
            'name': 'Обновлённый проект',
            'description': 'Новое описание',
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data['id'] == project['id']
    assert data['name'] == 'Обновлённый проект'
    assert data['description'] == 'Новое описание'


async def test_delete_project(
    client,
    auth_headers,
    company,
    project,
):
    endpoint = f'/companies/{company["id"]}/projects/{project["id"]}'
    response = await client.delete(endpoint, headers=auth_headers)
    assert response.status_code == 204

    response = await client.get(endpoint, headers=auth_headers)
    assert response.status_code == 404


async def test_cannot_access_foreign_project(
    client,
    company,
    project,
    foreign_auth_headers,
):
    response = await client.get(
        f'/companies/{company["id"]}/projects/{project["id"]}',
        headers=foreign_auth_headers,
    )
    assert response.status_code == 404


async def test_cannot_create_project_in_foreign_company(
    client,
    company,
    foreign_auth_headers,
):
    response = await client.post(
        f'/companies/{company["id"]}/projects',
        headers=foreign_auth_headers,
        json={
            'name': 'Чужой проект',
        },
    )
    assert response.status_code == 404
