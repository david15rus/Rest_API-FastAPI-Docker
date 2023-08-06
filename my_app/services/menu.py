from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.repositories import menu_repository
from my_app.schemas.menu import MenuSchema, MenuSchemaAdd, MenuSchemaUpdate


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
