from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.config import get_session
from my_app.schemas.menu import MenuSchema, MenuSchemaAdd, MenuSchemaUpdate
from my_app.services.menu import MenuService

router = APIRouter()

menu_service = MenuService()


@router.post("/", response_model=MenuSchema)
async def create_menu(menu_data: MenuSchemaAdd, session: AsyncSession = Depends(get_session)):
    """
    Получает все записи из БД из таблицы Menu.

    Parameters:
        skip (int): Число записей, которое следует пропустить перед возвратом
        limit (int): Максимальное количество записей, которые следует вернуть.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ с информацией о меню.
    """
    new_menu = await menu_service.create_menu(menu_data, session)
    return JSONResponse(
        content={
            "id": str(new_menu.id),
            "title": new_menu.title,
            "description": new_menu.description
        },
        status_code=201)


@router.get("/", response_model=None)
async def read_menus(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)):
    """
    Получает запись из БД из таблицы Menu по указанному идентификатору.

    Parameters:
        menu_id (str): Идентификатор меню.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ с информацией о меню.

    Raises:
        HTTPException: Если меню с указанным идентификатором
        не найдено в базе данных.
    """
    menus = await menu_service.read_menus(skip, limit, session)
    return JSONResponse(content=menus, status_code=200)


@router.get("/{menu_id}", response_model=None)
async def read_one_menu(menu_id: str, session: AsyncSession = Depends(get_session)):
    """
    Получает запись из БД из таблицы Menu по указанному идентификатору.

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
    return JSONResponse(content=menu, status_code=200)


@router.patch("/{menu_id}", response_model=None)
async def update_menu(menu_id: str, menu_data: MenuSchemaUpdate, session: AsyncSession = Depends(get_session)):
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
    return JSONResponse(content=updated_menu, status_code=200)


@router.delete("/{menu_id}", response_model=None)
async def delete_menu(menu_id: str, session: AsyncSession = Depends(get_session)):
    """
    Удаляет запись из БД из таблицы Menu по указанному идентификатору.

    Parameters:
        menu_id (str): Идентификатор меню, которое необходимо удалить.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns: JSONResponse: Пустой JSON-ответ с кодом 200 в случае успешного
    удаления.

    Raises:
        HTTPException: Если меню с указанным идентификатором не найдено в
        базе данных.
    """
    removed_menu = await menu_service.delete_menu(menu_id, session)
    if removed_menu:
        return JSONResponse(content={}, status_code=200)

    raise HTTPException(status_code=404, detail="menu not found")