from typing import Any

from sqlalchemy import ScalarResult, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.models.models import Dish, SubMenu
from my_app.schemas.submenu import SubMenuSchema, SubMenuSchemaAdd, SubMenuSchemaUpdate


async def create_submenu(menu_id: str,
                         submenu_data: SubMenuSchemaAdd,
                         session: AsyncSession) -> SubMenuSchema:
    new_submenu = SubMenu(title=submenu_data.title, description=submenu_data.description, menu_id=menu_id)
    session.add(new_submenu)
    await session.commit()
    await session.refresh(new_submenu)

    return SubMenuSchema(
        id=str(new_submenu.id),
        title=new_submenu.title,
        description=new_submenu.description,
        menu_id=menu_id,
    )


async def get_all_submenus(menu_id: str,
                           skip: int,
                           limit: int,
                           session: AsyncSession) -> ScalarResult[Any]:
    submenus = await session.execute(select(SubMenu).filter(
        SubMenu.menu_id == menu_id).offset(skip).limit(limit))
    return submenus.scalars()


async def get_submenu_by_id(menu_id: str, submenu_id: str, session: AsyncSession) -> SubMenuSchema | None:
    submenu = await session.execute(select(SubMenu).filter(
        SubMenu.id == submenu_id, SubMenu.menu_id == menu_id))

    return submenu.scalar_one_or_none()


async def update_submenu_by_id(menu_id: str,
                               submenu_id: str,
                               submenu_data: SubMenuSchemaUpdate,
                               session: AsyncSession) -> SubMenuSchemaUpdate:
    updated_submenu = await session.execute(select(SubMenu).filter(
        SubMenu.id == submenu_id, SubMenu.menu_id == menu_id))
    updated_submenu = updated_submenu.scalar_one_or_none()

    updated_submenu.title = submenu_data.title
    updated_submenu.description = submenu_data.description
    await session.commit()
    await session.refresh(updated_submenu)

    return updated_submenu


async def delete_submenu(submenu_id: str, session: AsyncSession) -> SubMenuSchema:
    query = select(SubMenu).filter(
        SubMenu.id == submenu_id)
    removed_submenu = await session.execute(query)
    removed_submenu = removed_submenu.scalar_one_or_none()

    await session.delete(removed_submenu)
    await session.commit()

    return removed_submenu


async def get_dish_count(submenu_id: str, session: AsyncSession) -> int:
    query = select(func.count(Dish.id)).filter(Dish.submenu_id == submenu_id)
    result = await session.execute(query)
    dishes_count = result.scalar()

    return dishes_count
