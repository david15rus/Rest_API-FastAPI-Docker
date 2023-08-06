from cashews import cache
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.config import get_session
from my_app.schemas.dish import DishSchema, DishSchemaAdd, DishSchemaUpdate
from my_app.services.dish_service import DishService

router = APIRouter()

dish_service = DishService()


@router.get('/', response_model=DishSchema, name='get_dishes')
@cache(ttl='2m')
async def read_dish(submenu_id: str, skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)) -> JSONResponse:
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
    response_data = []
    for dish in dishes:
        response_data.append(
            {
                'id': dish.id,
                'title': dish.title,
                'description': dish.description,
                'price': str(dish.price),
            }
        )
    return JSONResponse(content=response_data, status_code=200)


@router.get('/{dish_id}', response_model=DishSchema, name='get_dish')
@cache(ttl='2m')
async def read_one_dish(submenu_id: str, dish_id: str, session: AsyncSession = Depends(get_session)) -> JSONResponse:
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
    return JSONResponse(
        content={
            'id': dish.id,
            'title': dish.title,
            'description': dish.description,
            'price': str(dish.price),
        },
        status_code=200)


@router.post('/', response_model=DishSchema, name='post_dish')
@cache.invalidate(read_dish)
@cache.invalidate(read_one_dish)
async def create_dish(submenu_id: str, dish_data: DishSchemaAdd, session: AsyncSession = Depends(get_session)) -> JSONResponse:
    """
    Добавляет запись в БД в таблице Dish для указанного подменю по id.

    Parameters
        submenu_id (str): Идентификатор подменю, для которого получается список блюд.
        dish_data (DishSchemaAdd): Данные для добавления блюда.
        session (AsyncSession): Асинхронная сессия с базой данных.

    Returns:
        JSONResponse: Ответ со списком блюд для указанного подменю.
    """
    new_dish = await dish_service.create_dish(submenu_id, dish_data, session)
    return JSONResponse(
        content={
            'id': new_dish.id,
            'title': new_dish.title,
            'description': new_dish.description,
            'price': str(new_dish.price),
        },
        status_code=201)


@router.patch('/{dish_id}', response_model=DishSchema, name='patch_dish')
@cache.invalidate(read_dish)
@cache.invalidate(read_one_dish)
async def update_dish(submenu_id: str, dish_id: str, dish_data: DishSchemaUpdate, session: AsyncSession = Depends(get_session)) -> JSONResponse:
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
    return JSONResponse(
        content={
            'id': updated_dish.id,
            'title': updated_dish.title,
            'description': updated_dish.description,
            'price': str(updated_dish.price),
        },
        status_code=200)


@router.delete('/{dish_id}', response_model=None, name='delete_dish')
@cache.invalidate(read_dish)
@cache.invalidate(read_one_dish)
async def delete_dish(submenu_id: str, dish_id: str, session: AsyncSession = Depends(get_session)) -> JSONResponse:
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

    raise HTTPException(status_code=404, detail='dish not found')
