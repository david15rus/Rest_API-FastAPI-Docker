from typing import Any

from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.models.models import Dish
from my_app.schemas.dish import DishSchema, DishSchemaAdd, DishSchemaUpdate


async def create_dish(submenu_id: str,
                      dish_data: DishSchemaAdd,
                      session: AsyncSession) -> DishSchema:
    if dish_data.id:
        new_dish = Dish(
            id=dish_data.id,
            title=dish_data.title,
            description=dish_data.description,
            submenu_id=submenu_id,
            price=float(dish_data.price)
        )
    else:
        new_dish = Dish(
            title=dish_data.title,
            description=dish_data.description,
            submenu_id=submenu_id,
            price=float(dish_data.price)
        )
    session.add(new_dish)
    await session.commit()
    await session.refresh(new_dish)

    return new_dish


async def get_all_dishes(submenu_id: str,
                         skip: int,
                         limit: int,
                         session: AsyncSession) -> ScalarResult[Any]:
    dishes = await session.execute(select(Dish).filter(
        Dish.submenu_id == submenu_id).offset(skip).limit(limit))
    return dishes.scalars()


async def get_dish_by_id(submenu_id: str, dish_id: str, session: AsyncSession) -> DishSchema | None:
    dish = await session.execute(select(Dish).filter(
        Dish.id == dish_id, Dish.submenu_id == submenu_id))

    return dish.scalar_one_or_none()


async def update_dish_by_id(submenu_id: str,
                            dish_id: str,
                            dish_data: DishSchemaUpdate,
                            session: AsyncSession) -> DishSchemaUpdate:
    updated_dish = await session.execute(select(Dish).filter(
        Dish.id == dish_id, Dish.submenu_id == submenu_id))
    updated_dish = updated_dish.scalar_one_or_none()

    updated_dish.title = dish_data.title
    updated_dish.description = dish_data.description
    updated_dish.price = float(dish_data.price)
    await session.commit()
    await session.refresh(updated_dish)

    return updated_dish


async def delete_dish(submenu_id: str, dish_id: str, session: AsyncSession) -> DishSchema:
    query = select(Dish).filter(
        Dish.id == dish_id, Dish.submenu_id == submenu_id)
    removed_submenu = await session.execute(query)
    removed_submenu = removed_submenu.scalar_one_or_none()

    await session.delete(removed_submenu)
    await session.commit()

    return removed_submenu
