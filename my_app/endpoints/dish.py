from typing import Any

from cashews import cache
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.config import get_session
from my_app.schemas.dish import DishSchema, DishSchemaAdd, DishSchemaUpdate
from my_app.services.dish_service import DishService

router = APIRouter()

dish_service = DishService()


@router.get('/', response_model=list[DishSchema], name='get_dishes', status_code=200)
@cache(ttl='2m')
async def read_dishes(submenu_id: str,
                      skip: int = 0,
                      limit: int = 10,
                      session: AsyncSession = Depends(get_session)) -> list[DishSchema]:
    """
    Получает список блюд для указанного подменю.

    Parameters:
       submenu_id (str): Идентификатор подменю.
       skip (int, optional): Количество пропускаемых блюд.
       limit (int, optional): Максимальное количество возвращаемых блюд.
       session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
       JSONResponse: Список блюд для указанного подменю.
    """
    dishes = await dish_service.read_dishes(submenu_id, skip, limit, session)
    return dishes


@router.get('/{dish_id}', response_model=DishSchema, name='get_dish', status_code=200)
@cache(ttl='2m')
async def read_one_dish(submenu_id: str,
                        dish_id: str,
                        session: AsyncSession = Depends(get_session)) -> DishSchema:
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
    return dish


@router.post('/', response_model=DishSchema, name='post_dish', status_code=201)
async def create_dish(submenu_id: str,
                      dish_data: DishSchemaAdd,
                      background_tasks: BackgroundTasks,
                      session: AsyncSession = Depends(get_session)) -> DishSchema:
    """
    Добавляет запись в БД в таблице Dish для указанного подменю по id.

    Parameters
        submenu_id (str): Идентификатор подменю, для которого получается список блюд.
        dish_data (DishSchemaAdd): Данные для добавления блюда.
        background_tasks (BackgroundTasks): Объект для работы с фоновыми задачами.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ со списком блюд для указанного подменю.
    """
    new_dish = await dish_service.create_dish(submenu_id, dish_data, session)
    background_tasks.add_task(cache.invalidate, read_dishes)
    background_tasks.add_task(cache.invalidate, read_one_dish)
    return new_dish


@router.patch('/{dish_id}', response_model=DishSchema, name='patch_dish', status_code=200)
async def update_dish(submenu_id: str,
                      dish_id: str,
                      dish_data: DishSchemaUpdate,
                      background_tasks: BackgroundTasks,
                      session: AsyncSession = Depends(get_session)) -> DishSchema:
    """
    Обновляет информацию о блюде в указанном подменю.

    Parameters:
        submenu_id (str): Идентификатор подменю, к которому относится блюдо.
        dish_id (str): Идентификатор блюда, которое требуется обновить.
        dish_data (DishSchemaUpdate): Обновленные данные для блюда.
        background_tasks (BackgroundTasks): Объект для работы с фоновыми задачами.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ с информацией об обновленном блюде.
    """
    updated_dish = await dish_service.update_dish(submenu_id, dish_id, dish_data, session)
    background_tasks.add_task(cache.invalidate, read_dishes)
    background_tasks.add_task(cache.invalidate, read_one_dish)
    return updated_dish


@router.delete('/{dish_id}', response_model=None, name='delete_dish', status_code=200)
async def delete_dish(submenu_id: str,
                      dish_id: str,
                      background_tasks: BackgroundTasks,
                      session: AsyncSession = Depends(get_session)) -> dict[Any, Any]:
    """
    Удаляет указанное блюдо из подменю.

    Parameters:
        submenu_id (str): Идентификатор подменю.
        dish_id (str): Идентификатор удаляемого блюда.
        background_tasks (BackgroundTasks): Объект для работы с фоновыми задачами.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Пустой ответ, если блюдо успешно удалено.

    Raises:
        HTTPException: Если указанное блюдо не найдено в подменю.
    """
    removed_dish = await dish_service.delete_dish(submenu_id, dish_id, session)
    if removed_dish:
        background_tasks.add_task(cache.invalidate, read_dishes)
        background_tasks.add_task(cache.invalidate, read_one_dish)
        return {}

    raise HTTPException(status_code=404, detail='dish not found')
