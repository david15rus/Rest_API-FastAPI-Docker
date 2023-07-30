from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.config import get_session
from my_app.schemas.dish import DishSchemaUpdate, DishSchemaAdd
from my_app.services.dish_service import DishService

router = APIRouter()

dish_service = DishService()


@router.post("/", response_model=None)
async def create_dish(submenu_id: str, dish_data: DishSchemaAdd, session: AsyncSession = Depends(get_session)):
    """
    Получает список блюд для указанного подменю.

    Parameters:
        menu_id (str): Идентификатор меню, к которому относится подменю.
        submenu_id (str): Идентификатор подменю, для которого получается список блюд.
        skip (int): Количество пропускаемых блюд.
        limit (int): Максимальное количество блюд в списке.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ со списком блюд для указанного подменю.
    """
    new_dish = await dish_service.create_dish(submenu_id, dish_data, session)
    return JSONResponse(
        content={
            "id": str(new_dish.id),
            "title": new_dish.title,
            "description": new_dish.description,
            "price": str(round(new_dish.price, 2)),
        },
        status_code=201)

@router.get("/", response_model=None)
async def read_dish(submenu_id: str, skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)):
    """
    Получает список блюд для указанного подменю.

    Parameters:
       menu_id (str): Идентификатор меню.
       submenu_id (str): Идентификатор подменю.
       skip (int): Количество пропускаемых блюд.
       limit (int): Максимальное количество возвращаемых блюд.
       session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
       JSONResponse: Список блюд для указанного подменю.
    """
    dishes = await dish_service.read_dishes(submenu_id, skip, limit, session)
    return JSONResponse(content=dishes, status_code=200)


@router.get("/{dish_id}", response_model=None)
async def read_one_dish(submenu_id: str, dish_id: str, session: AsyncSession = Depends(get_session)):
    """
    Получает информацию о конкретном блюде для указанного подменю.

    Parameters:
        submenu_id (str): Идентификатор подменю, к которому относится блюдо.
        dish_id (str): Идентификатор блюда.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ с информацией о блюде.

    Raises:
        HTTPException: Если блюдо не найдено.
    """
    dish = await dish_service.read_one_dish(submenu_id, dish_id, session)
    return JSONResponse(content=dish, status_code=200)


@router.patch("/{dish_id}", response_model=None)
async def update_dish(submenu_id: str, dish_id: str, dish_data: DishSchemaUpdate, session: AsyncSession = Depends(get_session)):
    """
    Обновляет информацию о блюде в указанном подменю.

    Parameters:
        submenu_id (str): Идентификатор подменю, к которому относится блюдо.
        dish_id (str): Идентификатор блюда, которое требуется обновить.
        dish_data (DishSchemaUpdate): Обновленные данные для блюда.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ с информацией об обновленном блюде.
    """
    updated_dish = await dish_service.update_dish(submenu_id, dish_id, dish_data, session)
    return JSONResponse(content=updated_dish, status_code=200)


@router.delete("/{dish_id}", response_model=None)
async def delete_dish(submenu_id: str, dish_id: str, session: AsyncSession = Depends(get_session)):
    """
    Удаляет указанное блюдо из подменю.

    Parameters:
        menu_id (str): Идентификатор меню.
        submenu_id (str): Идентификатор подменю.
        dish_id (str): Идентификатор удаляемого блюда.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Пустой ответ, если блюдо успешно удалено.

    Raises:
        HTTPException: Если указанное блюдо не найдено в подменю.
    """
    removed_dish = await dish_service.delete_dish(submenu_id, dish_id, session)
    if removed_dish:
        return JSONResponse(content={}, status_code=200)

    raise HTTPException(status_code=404, detail="dish not found")
