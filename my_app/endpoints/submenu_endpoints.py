from typing import Any

from cashews import cache
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.config import get_session
from my_app.schemas.submenu_schema import (
    SubMenuSchema,
    SubMenuSchemaAdd,
    SubMenuSchemaUpdate,
)
from my_app.services.submenu_service import SubMenuService

router = APIRouter()

submenu_service = SubMenuService()


@router.get('/', response_model=list[SubMenuSchema], name='get_submenus', status_code=200)
@cache(ttl='2m')
async def read_submenus(menu_id: str,
                        skip: int = 0,
                        limit: int = 10,
                        session: AsyncSession = Depends(get_session)) -> list[SubMenuSchema]:
    """
    Получает все записи из БД из таблицы SubMenu для указанного меню по его id.

    Parameters:
       menu_id (str): Идентификатор меню, для которого нужно получить список подменю.
       skip (int, optional): Количество записей, которое нужно пропустить.
       limit (int, optional): Максимальное количество записей для возврата.
       session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
       JSONResponse: JSON-ответ с информацией о подменю c кодом 200.
    """
    submenus = await submenu_service.read_submenus(menu_id, skip, limit, session)
    return submenus


@router.get('/{submenu_id}', response_model=SubMenuSchema, name='get_submenu', status_code=200)
@cache(ttl='2m')
async def read_one_submenu(menu_id: str,
                           submenu_id: str,
                           session: AsyncSession = Depends(get_session)) -> SubMenuSchema:
    """
    Получает одну запись о конкретном подменю из БД из таблицы SubMenu
    для указанного меню по его id.

    Parameters:
        menu_id (str): Идентификатор меню, к которому принадлежит подменю.
        submenu_id (str): Идентификатор подменю, которое нужно получить.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: JSON-ответ с информацией о подменю с кодом 200.

    Raises:
        HTTPException: Если меню или подменю с указанными идентификаторами не
        найдены в базе данных.
    """
    submenu = await submenu_service.read_one_submenu(menu_id, submenu_id, session)
    return submenu


@router.post('/', response_model=SubMenuSchema, name='post_submenu', status_code=201)
async def create_submenu(menu_id: str,
                         submenu_data: SubMenuSchemaAdd,
                         background_tasks: BackgroundTasks,
                         session: AsyncSession = Depends(get_session)) -> SubMenuSchema:
    """
    Добавляет запись в БД в таблице SubMenu для указанного меню по id.

    Parameters:
        menu_id (str): Идентификатор меню, к которому добавляется подменю.
        submenu_data (SubMenuSchemaAdd): Данные для создания нового подменю.
        background_tasks (BackgroundTasks): Объект для работы с фоновыми задачами.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: JSON-ответ с информацией о созданном подменю и кодом 201.
    """
    new_submenu = await submenu_service.create_submenu(menu_id, submenu_data, session)
    background_tasks.add_task(cache.invalidate, read_submenus)
    background_tasks.add_task(cache.invalidate, read_one_submenu)
    return new_submenu


@router.patch('/{submenu_id}', response_model=None, name='patch_submenu', status_code=200)
async def update_submenu(menu_id: str,
                         submenu_id: str,
                         submenu_data: SubMenuSchemaUpdate,
                         background_tasks: BackgroundTasks,
                         session: AsyncSession = Depends(get_session)) -> SubMenuSchema:
    """
    Обновляет запись в БД в таблице SubMenu по указанному идентификатору
    подменю для указанного меню.

    Parameters:
       menu_id (str): Идентификатор меню, к которому принадлежит подменю.
       submenu_id (str): Идентификатор подменю, которое нужно обновить.
       submenu_data (SubMenuSchemaUpdate): данные для обновления записи.
       background_tasks (BackgroundTasks): Объект для работы с фоновыми задачами.
       session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
       JSONResponse: JSON-ответ с обновленной информацией о подменю и
       кодом 200.

    Raises:
       HTTPException: Если меню или подменю с указанными идентификаторами не
       найдены в базе данных.
    """
    updated_submenu = await submenu_service.update_submenu(menu_id, submenu_id, submenu_data, session)
    background_tasks.add_task(cache.invalidate, read_submenus)
    background_tasks.add_task(cache.invalidate, read_one_submenu)
    return updated_submenu


@router.delete('/{submenu_id}', response_model=None, name='delete_submenu', status_code=200)
async def delete_submenu(submenu_id: str,
                         background_tasks: BackgroundTasks,
                         session: AsyncSession = Depends(get_session)) -> dict[Any, Any]:
    """
    Удаляет запись из БД из таблицы SubMenu по указанному идентификатору
    подменю для указанного меню.

    Parameters:
        submenu_id (str): Идентификатор подменю, которое нужно удалить.
        background_tasks (BackgroundTasks): Объект для работы с фоновыми задачами.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Пустой JSON-ответ и код 200 в случае успешного удаления.

    Raises:
        HTTPException: Если меню или подменю с указанными идентификаторами
        не найдены в базе данных.
    """
    removed_submenu = await submenu_service.delete_submenu(submenu_id, session)
    if removed_submenu:
        background_tasks.add_task(cache.invalidate, read_submenus)
        background_tasks.add_task(cache.invalidate, read_one_submenu)
        return {}

    raise HTTPException(status_code=404, detail='submenu not found')
