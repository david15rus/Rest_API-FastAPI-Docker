from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.repositories import menu_repository
from my_app.schemas.dish_schema import DishSchema
from my_app.schemas.menu_schema import (
    MenuSchema,
    MenuSchemaAdd,
    MenuSchemaUpdate,
    MenuSchemaWithAll,
)
from my_app.schemas.submenu_schema import SubMenuSchemaWithDish


class MenuService:
    @staticmethod
    async def create_menu(menu_data: MenuSchemaAdd, session: AsyncSession) -> MenuSchema:
        new_menu = await menu_repository.create_menu(menu_data, session)

        return MenuSchema(
            id=str(new_menu.id),
            title=new_menu.title,
            description=new_menu.description
        )

    @staticmethod
    async def read_menus(skip: int, limit: int, session: AsyncSession) -> list[
            MenuSchema]:
        menus = await menu_repository.get_all_menus(skip, limit, session)

        response_data = []
        for menu in menus:
            counter = await menu_repository.get_dish_and_submenus_count(menu.id, session)
            response_data.append(
                MenuSchema(
                    id=str(menu.id),
                    title=menu.title,
                    description=menu.description,
                    submenus_count=int(counter['submenus_count']),
                    dishes_count=int(counter['dishes_count']),
                )
            )
        return response_data

    @staticmethod
    async def read_menus_with_submenus_and_dishes(session: AsyncSession):
        menus = await menu_repository.get_all_menu_with_submenus_and_dishes(session)

        response_data = []
        for menu in menus:
            submenu_data = []
            for submenu in menu.submenus:
                dish_data = []
                for dish in submenu.dishes:
                    # Добавляем информацию о блюде в список блюд
                    dish_data.append(
                        DishSchema(
                            id=str(dish.id),
                            title=dish.title,
                            description=dish.description,
                            price=str(round(float(dish.price), 2)),
                            submenu_id=str(dish.submenu_id)
                        )
                    )

                # Добавляем информацию о подменю и блюдах в список подменю
                submenu_data.append(
                    SubMenuSchemaWithDish(
                        id=str(submenu.id),
                        title=submenu.title,
                        description=submenu.description,
                        menu_id=str(submenu.menu_id),
                        dishes=dish_data
                    )
                )

            # Добавляем информацию о меню и подменю в список меню
            response_data.append(
                MenuSchemaWithAll(
                    id=str(menu.id),
                    title=menu.title,
                    description=menu.description,
                    submenus=submenu_data
                )
            )
        return response_data

    @staticmethod
    async def read_one_menu(menu_id: str, session: AsyncSession) -> MenuSchema:
        menu = await menu_repository.get_menu_by_id(menu_id, session)

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        counter = await menu_repository.get_dish_and_submenus_count(menu.id, session)

        return MenuSchema(
            id=str(menu.id),
            title=menu.title,
            description=menu.description,
            submenus_count=int(counter['submenus_count']),
            dishes_count=int(counter['dishes_count'])
        )

    @staticmethod
    async def update_menu(menu_id: str, menu_data: MenuSchemaUpdate, session: AsyncSession) -> MenuSchema:
        updated_menu = await menu_repository.update_menu_by_id(menu_id, menu_data, session)

        if not updated_menu:
            raise HTTPException(status_code=404, detail='menu not found')

        return MenuSchema(
            id=str(updated_menu.id),
            title=updated_menu.title,
            description=updated_menu.description
        )

    @staticmethod
    async def delete_menu(menu_id: str, session: AsyncSession) -> MenuSchema:
        deleted_menu = await menu_repository.delete_menu(menu_id, session)
        return MenuSchema(
            id=str(deleted_menu.id) if deleted_menu else None,
            title=deleted_menu.title if deleted_menu else None,
            description=deleted_menu.description if deleted_menu else None
        )
