from httpx import AsyncClient


async def test_create_dish(ac: AsyncClient):
    response = await ac.post('http://test/api/v1/menus/',
                             json={
                                "title": "Testing_menu3.1",
                                "description": "Testing_description3.1",
                             })
    menu_id = response.json()['id']

    response = await ac.post(f'http://test/api/v1/menus/{menu_id}/submenus/',
                             json={
                                "title": "Testing_submenu3.1",
                                "description": "Testing_description3.1",
                             })
    submenu_id = response.json()['id']

    response = await ac.post(f'http://test/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/',
                             json={
                                 "title": "Testing_dish3.1",
                                 "description": "Testing_description3.1",
                                 "price": 125.125
                             })

    assert response.status_code == 201

    dish_data = response.json()
    assert dish_data['title'] == "Testing_dish3.1"
    assert dish_data['description'] == "Testing_description3.1"
    assert dish_data['price'] == '125.12'
    assert dish_data['id'] is not None


async def test_read_dishes(ac: AsyncClient):
    response = await ac.post('http://test/api/v1/menus/',
                             json={
                                 "title": "Testing_menu3.2",
                                 "description": "Testing_description3.2",
                             })
    menu_id = response.json()['id']

    response = await ac.post(f'http://test/api/v1/menus/{menu_id}/submenus/',
                             json={
                                 "title": "Testing_submenu3.2",
                                 "description": "Testing_description3.2",
                             })
    submenu_id = response.json()['id']

    response = await ac.get(f'http://test/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/')

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


async def test_read_dish(ac: AsyncClient):
    response = await ac.post('http://test/api/v1/menus/',
                             json={
                                 "title": "Testing_menu3.3",
                                 "description": "Testing_description3.3",
                             })
    menu_id = response.json()['id']

    response = await ac.post(f'http://test/api/v1/menus/{menu_id}/submenus/',
                             json={
                                 "title": "Testing_submenu3.3",
                                 "description": "Testing_description3.3",
                             })
    submenu_id = response.json()['id']

    response = await ac.post(f'http://test/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/',
                             json={
                                 "title": "Testing_dish3.3",
                                 "description": "Testing_description3.3",
                                 "price": 125.125
                             })
    dish_id = response.json()['id']
    assert response.status_code == 201

    response = await ac.get(f'http://test/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')

    assert response.status_code == 200

    data = response.json()
    assert data['title'] == "Testing_dish3.3"
    assert data['description'] == "Testing_description3.3"
    assert data['price'] == '125.12'
    assert data['id'] is not None


async def test_update_dish(ac: AsyncClient):
    response = await ac.post('http://test/api/v1/menus/',
                             json={
                                 "title": "Testing_menu3.4",
                                 "description": "Testing_description3.4",
                             })
    menu_id = response.json()['id']

    response = await ac.post(f'http://test/api/v1/menus/{menu_id}/submenus/',
                             json={
                                 "title": "Testing_submenu3.4",
                                 "description": "Testing_description3.4",
                             })
    submenu_id = response.json()['id']

    response = await ac.post(
        f'http://test/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/',
        json={
            "title": "Testing_dish3.4",
            "description": "Testing_description3.4",
            "price": 125.125
        })
    dish_id = response.json()['id']

    response = await ac.patch(f'http://test/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
                              json={
                                "title": "Change_title",
                                "description": "Change_description",
                                "price": 255.255
                              })
    assert response.status_code == 200

    data = response.json()
    assert data['title'] == "Change_title"
    assert data['description'] == "Change_description"
    assert data['price'] == '255.25'
    assert data['id'] is not None


async def test_delete_submenu(ac: AsyncClient):
    response = await ac.post('http://test/api/v1/menus/',
                             json={
                                 "title": "Testing_menu3.5",
                                 "description": "Testing_description3.5",
                             })
    menu_id = response.json()['id']

    response = await ac.post(f'http://test/api/v1/menus/{menu_id}/submenus/',
                             json={
                                 "title": "Testing_submenu3.5",
                                 "description": "Testing_description3.5",
                             })
    submenu_id = response.json()['id']

    response = await ac.post(
        f'http://test/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/',
        json={
            "title": "Testing_dish3.5",
            "description": "Testing_description3.5",
            "price": 125.125
        })
    dish_id = response.json()['id']

    response = await ac.delete(f'http://test/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200

    data = response.json()
    assert data == {}
