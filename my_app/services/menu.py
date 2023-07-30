from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from my_app.repositories import menu_repository
from my_app.schemas.menu import MenuSchemaAdd, MenuSchema, MenuSchemaUpdate


class MenuService:
    async def create_menu(self, menu_data: MenuSchemaAdd, session):
        new_menu = await menu_repository.create_menu(menu_data, session)

        return new_menu

    async def read_menus(self, skip: int, limit: int, session):
        menus = await menu_repository.get_all_menus(skip, limit, session)

        response_data = []
        for menu in menus:
            counter = await menu_repository.get_dish_and_submenus_count(menu.id, session)
            response_data.append(
                {
                    "id": str(menu.id),
                    "title": menu.title,
                    "description": menu.description,
                    "submenus_count": counter['submenus_count'],
                    "dishes_count": counter['dishes_count'],
                }
            )
        return response_data

    async def read_one_menu(self, menu_id: str, session):
        menu = await menu_repository.get_menu_by_id(menu_id, session)

        if not menu:
            raise HTTPException(status_code=404, detail="menu not found")

        counter = await menu_repository.get_dish_and_submenus_count(menu.id, session)
        response_data = {
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description,
            "submenus_count": counter['submenus_count'],
            "dishes_count": counter['dishes_count'],
        }
        return response_data

    async def update_menu(self, menu_id: str, menu_data: MenuSchemaUpdate, session):
        updated_menu = await menu_repository.update_menu_by_id(menu_id, menu_data, session)

        if not updated_menu:
            raise HTTPException(status_code=404, detail="menu not found")

        response_data = {
            "id": str(updated_menu.id),
            "title": updated_menu.title,
            "description": updated_menu.description,
        }
        return response_data

    async def delete_menu(self, menu_id: str, session):
        deleted_menu = await menu_repository.delete_menu(menu_id, session)
        return deleted_menu
