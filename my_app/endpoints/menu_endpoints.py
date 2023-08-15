from typing import Any

from cashews import cache
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.config import get_session
from my_app.schemas.menu_schema import (
    MenuSchema,
    MenuSchemaAdd,
    MenuSchemaUpdate,
    MenuSchemaWithAll,
)
from my_app.services.menu_service import MenuService

router = APIRouter()

menu_service = MenuService()


@router.get('/', response_model=list[MenuSchema], name='get_menus', status_code=200)
@cache(ttl='2m')
async def read_menus(skip: int = 0, limit: int = 10,
                     session: AsyncSession = Depends(get_session)) -> list[MenuSchema]:
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
    return menus


@router.get('/all', response_model=list[MenuSchemaWithAll], name='get_menus_with_all', status_code=200)
@cache(ttl='2m')
async def read_menus_with_all(session: AsyncSession = Depends(get_session)) -> list[MenuSchemaWithAll]:
    """
    Получает все записи из БД из таблицы Menu со связными блюдами и подменю.

    Parameters:
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ с информацией о меню.
    """
    menus = await menu_service.read_menus_with_submenus_and_dishes(session)
    return menus


@router.get('/{menu_id}', response_model=MenuSchema, name='get_menu', status_code=200)
@cache(ttl='2m')
async def read_one_menu(menu_id: str,
                        session: AsyncSession = Depends(get_session)) -> MenuSchema:
    """
    Получает одну запись из БД из таблицы Menu по указанному идентификатору.

    Parameters:
        menu_id (str): Идентификатор меню.        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ с информацией о меню.

    Raises:
        HTTPException: Если меню с указанным идентификатором
        не найдено в базе данных.
    """
    menu = await menu_service.read_one_menu(menu_id, session)
    return menu


@router.post('/', response_model=MenuSchema, name='post_menu', status_code=201)
async def create_menu(menu_data: MenuSchemaAdd,
                      background_tasks: BackgroundTasks,
                      session: AsyncSession = Depends(get_session)) -> MenuSchema:
    """
    Добавляет запись в БД в таблицу Menu.

    Parameters:
        menu_data (MenuSchemaAdd): Данные для добавления меню.
        background_tasks (BackgroundTasks): Объект для работы с фоновыми задачами.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ с информацией о меню.
    """
    new_menu = await menu_service.create_menu(menu_data, session)
    background_tasks.add_task(cache.invalidate, read_menus)
    background_tasks.add_task(cache.invalidate, read_one_menu)
    return new_menu


@router.patch('/{menu_id}', response_model=MenuSchema, name='patch_menu')
async def update_menu(menu_id: str,
                      menu_data: MenuSchemaUpdate,
                      background_tasks: BackgroundTasks,
                      session: AsyncSession = Depends(get_session)) -> MenuSchema:
    """
    Обновляет запись в БД в таблице Menu по указанному идентификатору.

    Parameters:
        menu_id (str): Идентификатор меню, которое необходимо обновить.
        menu_data (MenuSchemaUpdate): Данные для обновления меню.
        background_tasks (BackgroundTasks): Объект для работы с фоновыми задачами.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ с информацией о меню.

    Raises:
        HTTPException: Если меню с указанным идентификатором
        не найдено в базе данных.
    """
    updated_menu = await menu_service.update_menu(menu_id, menu_data, session)
    background_tasks.add_task(cache.invalidate, read_menus)
    background_tasks.add_task(cache.invalidate, read_one_menu)
    return updated_menu


@router.delete('/{menu_id}', response_model=None, name='delete_menu')
async def delete_menu(menu_id: str,
                      background_tasks: BackgroundTasks,
                      session: AsyncSession = Depends(get_session)) -> dict[Any, Any]:
    """
    Удаляет запись из БД из таблицы Menu по указанному идентификатору.

    Parameters:
        menu_id (str): Идентификатор меню, которое необходимо удалить.
        background_tasks (BackgroundTasks): Объект для работы с фоновыми задачами.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Пустой JSON-ответ с кодом 200 в случае успешного удаления.

    Raises:
        HTTPException: Если меню с указанным идентификатором не найдено в базе данных.
    """
    removed_menu = await menu_service.delete_menu(menu_id, session)
    if removed_menu:
        background_tasks.add_task(cache.invalidate, read_menus)
        background_tasks.add_task(cache.invalidate, read_one_menu)
        return {}

    raise HTTPException(status_code=404, detail='menu not found')
