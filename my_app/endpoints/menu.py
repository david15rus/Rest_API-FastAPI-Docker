from cashews import cache
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.config import get_session
from my_app.schemas.menu import MenuSchema, MenuSchemaAdd, MenuSchemaUpdate
from my_app.services.menu import MenuService

router = APIRouter()

menu_service = MenuService()


@router.get('/', response_model=list[MenuSchema], name='get_menus')
@cache(ttl='2m')
async def read_menus(skip: int = 0, limit: int = 10,
                     session: AsyncSession = Depends(get_session)) -> \
        JSONResponse:
    """
    Получает все записи из БД из таблицы Menu.

    Parameters:
        skip (int, optional): Количество записей, которое нужно пропустить.
        limit (int, optional): Максимальное количество записей для возврата.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ с информацией о меню.
    """
    menus = await menu_service.read_menus(skip, limit, session)
    response_data = []
    for menu in menus:
        response_data.append(
            {
                'id': menu.id,
                'title': menu.title,
                'description': menu.description,
                'submenus_count': menu.submenus_count,
                'dishes_count': menu.dishes_count,
            }
        )
    return JSONResponse(content=response_data, status_code=200)


@router.get('/{menu_id}', response_model=MenuSchema, name='get_menu')
@cache(ttl='2m')
async def read_one_menu(menu_id: str, session: AsyncSession = Depends(
        get_session)) -> JSONResponse:
    """
    Получает одну запись из БД из таблицы Menu по указанному идентификатору.

    Parameters:
        menu_id (str): Идентификатор меню.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ с информацией о меню.

    Raises:
        HTTPException: Если меню с указанным идентификатором
        не найдено в базе данных.
    """
    menu = await menu_service.read_one_menu(menu_id, session)
    return JSONResponse(
        content={
            'id': menu.id,
            'title': menu.title,
            'description': menu.description,
            'submenus_count': menu.submenus_count,
            'dishes_count': menu.dishes_count,
        },
        status_code=200)


@router.post('/', response_model=MenuSchema, name='post_menu')
@cache.invalidate(read_menus)
@cache.invalidate(read_one_menu)
async def create_menu(menu_data: MenuSchemaAdd,
                      session: AsyncSession = Depends(
                          get_session)) -> JSONResponse:
    """
    Добавляет запись в БД в таблицу Menu.

    Parameters:
        menu_data (MenuSchemaAdd): Данные для добавления меню.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ с информацией о меню.
    """
    new_menu = await menu_service.create_menu(menu_data, session)
    return JSONResponse(
        content={
            'id': new_menu.id,
            'title': new_menu.title,
            'description': new_menu.description,
            'submenus_count': new_menu.submenus_count,
            'dishes_count': new_menu.dishes_count,
        },
        status_code=201)


@router.patch('/{menu_id}', response_model=MenuSchema, name='patch_menu')
@cache.invalidate(read_menus)
@cache.invalidate(read_one_menu)
async def update_menu(menu_id: str, menu_data: MenuSchemaUpdate,
                      session: AsyncSession = Depends(
                          get_session)) -> JSONResponse:
    """
    Обновляет запись в БД в таблице Menu по указанному идентификатору.

    Parameters:
        menu_id (str): Идентификатор меню, которое необходимо обновить.
        menu_data (MenuSchemaUpdate): Данные для обновления меню.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ с информацией о меню.

    Raises:
        HTTPException: Если меню с указанным идентификатором
        не найдено в базе данных.
    """
    updated_menu = await menu_service.update_menu(menu_id, menu_data, session)
    return JSONResponse(
        content={
            'id': updated_menu.id,
            'title': updated_menu.title,
            'description': updated_menu.description,
            'submenus_count': updated_menu.submenus_count,
            'dishes_count': updated_menu.dishes_count,
        },
        status_code=200)


@router.delete('/{menu_id}', response_model=None, name='delete_menu')
@cache.invalidate(read_menus)
@cache.invalidate(read_one_menu)
async def delete_menu(menu_id: str, session: AsyncSession = Depends(
        get_session)) -> JSONResponse:
    """
    Удаляет запись из БД из таблицы Menu по указанному идентификатору.

    Parameters:
        menu_id (str): Идентификатор меню, которое необходимо удалить.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Пустой JSON-ответ с кодом 200 в случае успешного удаления.

    Raises:
        HTTPException: Если меню с указанным идентификатором не найдено в базе данных.
    """
    removed_menu = await menu_service.delete_menu(menu_id, session)
    if removed_menu:
        return JSONResponse(content={}, status_code=200)

    raise HTTPException(status_code=404, detail='menu not found')
