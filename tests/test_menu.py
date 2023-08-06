from conftest import app, async_session_maker
from httpx import AsyncClient
from starlette.datastructures import URLPath

from my_app.schemas.menu import MenuSchemaAdd
from my_app.services.menu import MenuService


async def test_create():
    async with async_session_maker() as session:
        menu_data = MenuSchemaAdd(title='Testing_menu1', description='Testing_description1')

        menu_service = MenuService()

        new_menu = await menu_service.create_menu(menu_data, session)

        assert new_menu.title == menu_data.title, 'Название неверно'
        assert new_menu.description == menu_data.description, 'Описание неверно'
        assert new_menu.id is not None, 'id не задан'


async def test_create_menu(ac: AsyncClient):
    # 'http://test/api/v1/menus/'
    url = URLPath(app.url_path_for('post_menu'))
    response = await ac.post(url, json={
        'title': 'Testing_menu2',
        'description': 'Testing_description2',
    })

    assert response.status_code == 201

    data = response.json()
    assert data['title'] == 'Testing_menu2'
    assert data['description'] == 'Testing_description2'
    assert data['id'] is not None


async def test_read_menus(ac: AsyncClient):
    url = URLPath(app.url_path_for('get_menus'))
    response = await ac.get(url)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


async def test_read_menu(ac: AsyncClient):
    url = URLPath(app.url_path_for('post_menu'))
    response = await ac.post(url, json={
        'title': 'Testing_menu3',
        'description': 'Testing_description3',
    })
    data = response.json()
    menu_id = data['id']
    url = URLPath(app.url_path_for('get_menu', menu_id=menu_id))
    response = await ac.get(url)

    assert response.status_code == 200

    data = response.json()
    assert data['title'] == 'Testing_menu3'
    assert data['description'] == 'Testing_description3'
    assert data['id'] is not None


async def test_update_menu(ac: AsyncClient):
    url = URLPath(app.url_path_for('post_menu'))
    response = await ac.post(url, json={
        'title': 'Testing_menu4',
        'description': 'Testing_description4',
    })
    data = response.json()
    menu_id = data['id']

    url = URLPath(app.url_path_for('patch_menu', menu_id=menu_id))
    response = await ac.patch(url, json={
        'title': 'Change_title',
        'description': 'Change_description',
    })
    assert response.status_code == 200

    data = response.json()
    assert data['title'] == 'Change_title'
    assert data['description'] == 'Change_description'
    assert data['id'] is not None


async def test_delete_menu(ac: AsyncClient):
    url = URLPath(app.url_path_for('post_menu'))
    response = await ac.post(url, json={
        'title': 'Testing_menu5',
        'description': 'Testing_description5',
    })
    data = response.json()
    menu_id = data['id']

    url = URLPath(app.url_path_for('delete_menu', menu_id=menu_id))
    response = await ac.delete(url)
    assert response.status_code == 200

    data = response.json()
    assert data == {}
