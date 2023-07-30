from typing import List, Optional

from sqlalchemy import select, func, distinct

from my_app.models.models import Menu, SubMenu, Dish
from my_app.schemas.menu import MenuSchemaAdd, MenuSchemaUpdate, MenuSchema


async def create_menu(menu_data: MenuSchemaAdd,
                      session
                      ) -> MenuSchema:
    new_menu = Menu(title=menu_data.title, description=menu_data.description)
    session.add(new_menu)
    await session.commit()
    await session.refresh(new_menu)

    return MenuSchema(
        id=str(new_menu.id),
        title=new_menu.title,
        description=new_menu.description
    )


async def get_all_menus(skip: int,
                        limit: int,
                        session
                        ):
    menus = await session.execute(select(Menu).offset(skip).limit(limit))

    return menus.scalars()


async def get_menu_by_id(menu_id: str, session) -> Optional[Menu]:
    menu = await session.execute(select(Menu).filter(Menu.id == menu_id))

    return menu.scalar_one_or_none()


async def update_menu_by_id(menu_id: str,
                            menu_data: MenuSchemaUpdate,
                            session):
    updated_menu = await session.execute(select(Menu).filter(Menu.id == menu_id))
    updated_menu = updated_menu.scalar_one_or_none()

    updated_menu.title = menu_data.title
    updated_menu.description = menu_data.description
    await session.commit()
    await session.refresh(updated_menu)

    return updated_menu


async def delete_menu(menu_id: str, session):
    query = select(Menu).filter(Menu.id == menu_id)
    removed_menu = await session.execute(query)
    removed_menu = removed_menu.scalar_one_or_none()

    await session.delete(removed_menu)
    await session.commit()

    return removed_menu


async def get_dish_and_submenus_count(menu_id: str,
                                      session
                                      ):
    submenus_table = SubMenu.__table__
    dishes_table = Dish.__table__

    query = (
        select(
            Menu,
            func.count(distinct(submenus_table.c.id)).label("submenus_count"),
            func.count(distinct(dishes_table.c.id)).label("dishes_count"),
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
        menu = row[0]
        submenus_count = row[1]
        dishes_count = row[2]
    else:
        submenus_count = 0
        dishes_count = 0

    return {'submenus_count': submenus_count, 'dishes_count': dishes_count}
