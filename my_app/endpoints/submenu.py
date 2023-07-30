from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.config import get_session
from my_app.schemas.submenu import SubMenuSchemaAdd, SubMenuSchemaUpdate
from my_app.services.submenu_service import SubMenuService

router = APIRouter()

submenu_service = SubMenuService()


@router.post("/", response_model=None)
async def create_submenu(menu_id: str, submenu_data: SubMenuSchemaAdd, session: AsyncSession = Depends(get_session)):
    """
    Добавляет запись в БД в таблице SubMenu для указанного меню по id.

    Parameters:
        menu_id (str): Идентификатор меню, к которому добавляется подменю.
        submenu_data (SubMenuSchemaAdd): Данные для создания нового подменю.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: JSON-ответ с информацией о созданном подменю и кодом 201.
    """
    new_submenu = await submenu_service.create_submenu(menu_id, submenu_data, session)
    return JSONResponse(
        content={
            "id": str(new_submenu.id),
            "title": new_submenu.title,
            "description": new_submenu.description
        },
        status_code=201)


@router.get("/", response_model=None)
async def read_submenus(menu_id: str, skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)):
    """
    Получает все записи из БД из таблицы SubMenu для указанного меню по его id.

    Parameters:
       menu_id (str): Идентификатор меню, для которого нужно получить список подменю.
       skip (int, optional): Количество записей, которое нужно пропустить.
       limit (int, optional): Максимальное количество записей для возврата.
       session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
       JSONResponse: JSON-ответ с информацией о подменю и кодом 200.
    """
    submenus = await submenu_service.read_submenus(menu_id, skip, limit, session)
    return JSONResponse(content=submenus, status_code=200)


@router.get("/{submenu_id}", response_model=None)
async def read_one_submenu(menu_id: str, submenu_id: str, session: AsyncSession = Depends(get_session)):
    """
    Получает одну запись о конкретном подменю из БД из таблицы SubMenu
    для указанного меню по его id.

    Parameters:
        menu_id (str): Идентификатор меню, к которому принадлежит подменю.
        submenu_id (str): Идентификатор подменю, которое нужно получить.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: JSON-ответ с информацией о подменю и кодом 200.

    Raises:
        HTTPException: Если меню или подменю с указанными идентификаторами не
        найдены в базе данных.
    """
    submenu = await submenu_service.read_one_submenu(menu_id, submenu_id, session)
    return JSONResponse(content=submenu, status_code=200)


@router.patch("/{submenu_id}", response_model=None)
async def update_submenu(menu_id: str, submenu_id: str, submenu_data: SubMenuSchemaUpdate, session: AsyncSession = Depends(get_session)):
    """
    Обновляет запись в БД в таблице SubMenu по указанному идентификатору
    подменю для указанного меню.

    Parameters:
       menu_id (str): Идентификатор меню, к которому принадлежит подменю.
       submenu_id (str): Идентификатор подменю, которое нужно обновить.
       submenu_data (SubMenuSchemaUpdate): данные для обновления записи.
       session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
       JSONResponse: JSON-ответ с обновленной информацией о подменю и
       кодом 200.

    Raises:
       HTTPException: Если меню или подменю с указанными идентификаторами не
       найдены в базе данных.
    """
    updated_submenu = await submenu_service.update_submenu(menu_id, submenu_id, submenu_data, session)
    return JSONResponse(content=updated_submenu, status_code=200)


@router.delete("/{submenu_id}", response_model=None)
async def delete_submenu(menu_id: str, submenu_id: str, session: AsyncSession = Depends(get_session)):
    """
    Удаляет запись из БД из таблицы SubMenu по указанному идентификатору
    подменю для указанного меню.

    Parameters:
        menu_id (str): Идентификатор меню, к которому принадлежит подменю.
        submenu_id (str): Идентификатор подменю, которое нужно удалить.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Пустой JSON-ответ и код 200 в случае успешного удаления.

    Raises:
        HTTPException: Если меню или подменю с указанными идентификаторами
        не найдены в базе данных.
    """
    removed_submenu = await submenu_service.delete_submenu(menu_id, submenu_id, session)
    if removed_submenu:
        return JSONResponse(content={}, status_code=200)

    raise HTTPException(status_code=404, detail="submenu not found")
