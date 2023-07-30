from fastapi import HTTPException
from my_app.repositories import submenu_repository
from my_app.schemas.submenu import SubMenuSchema, SubMenuSchemaAdd, SubMenuSchemaUpdate


class SubMenuService:
    @staticmethod
    async def create_submenu(menu_id: str, submenu_data: SubMenuSchemaAdd, session):
        new_submenu = await submenu_repository.create_submenu(menu_id, submenu_data, session)

        return new_submenu

    @staticmethod
    async def read_submenus(menu_id: str, skip: int, limit: int, session):
        submenus = await submenu_repository.get_all_submenus(menu_id, skip, limit, session)

        response_data = []
        for submenu in submenus:
            counter = await submenu_repository.get_dish_count(submenu.id, session)
            response_data.append(
                {
                    "id": str(submenu.id),
                    "title": submenu.title,
                    "description": submenu.description,
                    "dishes_count": counter,
                }
            )
        return response_data

    @staticmethod
    async def read_one_submenu(menu_id: str, submenu_id: str, session):
        submenu = await submenu_repository.get_submenu_by_id(menu_id, submenu_id, session)

        if not submenu:
            raise HTTPException(status_code=404, detail="submenu not found")

        counter = await submenu_repository.get_dish_count(submenu.id, session)
        response_data = {
            "id": str(submenu.id),
            "title": submenu.title,
            "description": submenu.description,
            "dishes_count": counter,
        }
        return response_data

    @staticmethod
    async def update_submenu(menu_id: str, submenu_id: str, submenu_data: SubMenuSchemaUpdate, session):
        updated_submenu = await submenu_repository.update_submenu_by_id(menu_id, submenu_id, submenu_data, session)

        if not updated_submenu:
            raise HTTPException(status_code=404, detail="menu not found")

        response_data = {
            "id": str(updated_submenu.id),
            "title": updated_submenu.title,
            "description": updated_submenu.description,
        }
        return response_data

    @staticmethod
    async def delete_submenu(menu_id: str, submenu_id: str, session):
        deleted_menu = await submenu_repository.delete_submenu(menu_id, submenu_id, session)
        return deleted_menu
