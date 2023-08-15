from sqlalchemy import ScalarResult, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from my_app.models.models import Dish, Menu, SubMenu
from my_app.schemas.menu_schema import MenuSchema, MenuSchemaAdd, MenuSchemaUpdate


async def create_menu(menu_data: MenuSchemaAdd,
                      session: AsyncSession
                      ) -> Menu:
    if menu_data.id:
        new_menu = Menu(id=menu_data.id, title=menu_data.title, description=menu_data.description)
    else:
        new_menu = Menu(title=menu_data.title, description=menu_data.description)

    session.add(new_menu)
    await session.commit()
    await session.refresh(new_menu)

    return new_menu


async def get_all_menus(skip: int,
                        limit: int,
                        session: AsyncSession
                        ) -> ScalarResult[MenuSchema]:
    menus = await session.execute(select(Menu).offset(skip).limit(limit))
    return menus.scalars()


async def get_all_menu_with_submenus_and_dishes(session: AsyncSession):
    query = (
        select(Menu)
        .options(selectinload(Menu.submenus).selectinload(SubMenu.dishes))
    )

    result = await session.execute(query)
    result = result.scalars()
    return result


async def get_menu_by_id(menu_id: str, session: AsyncSession) -> MenuSchema | None:
    menu = await session.execute(select(Menu).filter(Menu.id == menu_id))

    return menu.scalar_one_or_none()


async def update_menu_by_id(menu_id: str,
                            menu_data: MenuSchemaUpdate,
                            session: AsyncSession) -> MenuSchema | None:
    updated_menu = await session.execute(select(Menu).filter(Menu.id == menu_id))
    updated_menu = updated_menu.scalar_one_or_none()

    updated_menu.title = menu_data.title
    updated_menu.description = menu_data.description
    await session.commit()
    await session.refresh(updated_menu)

    return updated_menu


async def delete_menu(menu_id: str, session: AsyncSession) -> MenuSchema | None:
    query = select(Menu).filter(Menu.id == menu_id)
    removed_menu = await session.execute(query)
    removed_menu = removed_menu.scalar_one_or_none()

    await session.delete(removed_menu)
    await session.commit()

    return removed_menu


async def get_dish_and_submenus_count(menu_id: str,
                                      session: AsyncSession
                                      ) -> dict[str, int]:
    submenus_table = SubMenu.__table__
    dishes_table = Dish.__table__

    query = (
        select(
            Menu,
            func.count(distinct(submenus_table.c.id)).label('submenus_count'),
            func.count(distinct(dishes_table.c.id)).label('dishes_count'),
        )
        .select_from(Menu)
        .outerjoin(submenus_table, submenus_table.c.menu_id == Menu.id)
        .outerjoin(dishes_table,
                   dishes_table.c.submenu_id == submenus_table.c.id)
        .group_by(Menu.id)
        .filter(Menu.id == menu_id)
    )

    result = await session.execute(query)
    row = result.fetchone()

    if row:
        submenus_count = row[1]
        dishes_count = row[2]
    else:
        submenus_count = 0
        dishes_count = 0

    return {'submenus_count': submenus_count, 'dishes_count': dishes_count}
