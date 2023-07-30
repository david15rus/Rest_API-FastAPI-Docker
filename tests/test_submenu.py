from httpx import AsyncClient


async def test_create_submenu(ac: AsyncClient):
    response = await ac.post('http://test/api/v1/menus/', json={
        "title": "Testing_menu2.1",
        "description": "Testing_description2.1",
    })
    menu_id = response.json()['id']

    response = await ac.post(f'http://test/api/v1/menus/{menu_id}/submenus/',
                             json={
                                 "title": "Testing_submenu2.1",
                                 "description": "Testing_description2.1",
                             })

    assert response.status_code == 201

    submenu_data = response.json()
    assert submenu_data['title'] == "Testing_submenu2.1"
    assert submenu_data['description'] == "Testing_description2.1"
    assert submenu_data['id'] is not None


async def test_read_submenus(ac: AsyncClient):
    response = await ac.post('http://test/api/v1/menus/', json={
        "title": "Testing_menu2.2",
        "description": "Testing_description2.2",
    })
    menu_id = response.json()['id']

    response = await ac.get(f'http://test/api/v1/menus/{menu_id}/submenus/')

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


async def test_read_submenu(ac: AsyncClient):
    response = await ac.post('http://test/api/v1/menus/', json={
        "title": "Testing_menu2.3",
        "description": "Testing_description2.3",
    })
    menu_id = response.json()['id']

    response = await ac.post(f'http://test/api/v1/menus/{menu_id}/submenus/',
                             json={
                                 "title": "Testing_submenu2.2",
                                 "description": "Testing_description2.2",
                             })
    submenu_id = response.json()['id']
    assert response.status_code == 201

    response = await ac.get(f'http://test/api/v1/menus/{menu_id}/submenus/{submenu_id}')

    assert response.status_code == 200

    data = response.json()
    assert data['title'] == "Testing_submenu2.2"
    assert data['description'] == "Testing_description2.2"
    assert data['id'] is not None


async def test_update_submenu(ac: AsyncClient):
    response = await ac.post('http://test/api/v1/menus/', json={
        "title": "Testing_menu2.4",
        "description": "Testing_description2.4",
    })
    menu_id = response.json()['id']

    response = await ac.post(f'http://test/api/v1/menus/{menu_id}/submenus/',
                             json={
                                 "title": "Testing_submenu2.3",
                                 "description": "Testing_description2.3",
                             })
    submenu_id = response.json()['id']

    response = await ac.patch(f'http://test/api/v1/menus/{menu_id}/submenus/{submenu_id}', json={
        "title": "Change_title",
        "description": "Change_description",
    })
    assert response.status_code == 200

    data = response.json()
    assert data['title'] == "Change_title"
    assert data['description'] == "Change_description"
    assert data['id'] is not None


async def test_delete_submenu(ac: AsyncClient):
    response = await ac.post('http://test/api/v1/menus/', json={
        "title": "Testing_menu2.5",
        "description": "Testing_description2.5",
    })
    menu_id = response.json()['id']

    response = await ac.post(f'http://test/api/v1/menus/{menu_id}/submenus/',
                             json={
                                 "title": "Testing_submenu2.4",
                                 "description": "Testing_description2.4",
                             })
    submenu_id = response.json()['id']

    response = await ac.delete(f'http://test/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200

    data = response.json()
    assert data == {}
