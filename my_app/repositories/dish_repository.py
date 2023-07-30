from typing import List, Optional

from sqlalchemy import select, func

from my_app.models.models import Menu, SubMenu, Dish
from my_app.schemas.dish import DishSchema, DishSchemaAdd, DishSchemaUpdate


async def create_dish(submenu_id: str,
                      dish_data: DishSchemaAdd,
                      session):
    new_dish = Dish(title=dish_data.title, description=dish_data.description, submenu_id=submenu_id, price=dish_data.price)
    session.add(new_dish)
    await session.commit()
    await session.refresh(new_dish)

    return DishSchema(
        id=str(new_dish.id),
        title=new_dish.title,
        description=new_dish.description,
        price=str(round(new_dish.price, 2)),
        submenu_id=submenu_id,
    )


async def get_all_dishes(submenu_id: str,
                         skip: int,
                         limit: int,
                         session):
    dishes = await session.execute(select(Dish).filter(
        Dish.submenu_id == submenu_id).offset(skip).limit(limit))
    return dishes.scalars()


async def get_submenu_by_id(submenu_id: str, dish_id: str, session):
    dish = await session.execute(select(Dish).filter(
        Dish.id == dish_id, Dish.submenu_id == submenu_id))

    return dish.scalar_one_or_none()


async def update_dish_by_id(submenu_id: str,
                            dish_id: str,
                            dish_data: DishSchemaUpdate,
                            session):
    updated_dish = await session.execute(select(Dish).filter(
        Dish.id == dish_id, Dish.submenu_id == submenu_id))
    updated_dish = updated_dish.scalar_one_or_none()

    updated_dish.title = dish_data.title
    updated_dish.description = dish_data.description
    updated_dish.price = dish_data.price
    await session.commit()
    await session.refresh(updated_dish)

    return updated_dish


async def delete_dish(submenu_id: str, dish_id: str, session):
    query = select(Dish).filter(
        Dish.id == dish_id, Dish.submenu_id == submenu_id)
    removed_submenu = await session.execute(query)
    removed_submenu = removed_submenu.scalar_one_or_none()

    await session.delete(removed_submenu)
    await session.commit()

    return removed_submenu

