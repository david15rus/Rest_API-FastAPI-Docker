from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.repositories import submenu_repository
from my_app.schemas.submenu import SubMenuSchema, SubMenuSchemaAdd, SubMenuSchemaUpdate


class SubMenuService:
    @staticmethod
    async def create_submenu(menu_id: str, submenu_data: SubMenuSchemaAdd, session: AsyncSession) -> SubMenuSchema:
        new_submenu = await submenu_repository.create_submenu(menu_id, submenu_data, session)

        return SubMenuSchema(
            id=str(new_submenu.id),
            title=new_submenu.title,
            description=new_submenu.description,
            menu_id=str(new_submenu.menu_id)
        )

    @staticmethod
    async def read_submenus(menu_id: str, skip: int, limit: int, session: AsyncSession) -> \
            list[SubMenuSchema]:
        submenus = await submenu_repository.get_all_submenus(menu_id, skip, limit, session)

        response_data = []
        for submenu in submenus:
            counter = await submenu_repository.get_dish_count(submenu.id, session)
            response_data.append(
                SubMenuSchema(
                    id=str(submenu.id),
                    title=submenu.title,
                    description=submenu.description,
                    menu_id=str(submenu.menu_id),
                    dishes_count=int(counter)
                )
            )
        return response_data

    @staticmethod
    async def read_one_submenu(menu_id: str, submenu_id: str, session: AsyncSession) -> SubMenuSchema:
        submenu = await submenu_repository.get_submenu_by_id(menu_id, submenu_id, session)

        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        counter = await submenu_repository.get_dish_count(submenu.id, session)
        return SubMenuSchema(
            id=str(submenu.id),
            title=submenu.title,
            description=submenu.description,
            menu_id=str(submenu.menu_id),
            dishes_count=int(counter)
        )

    @staticmethod
    async def update_submenu(menu_id: str, submenu_id: str, submenu_data: SubMenuSchemaUpdate, session: AsyncSession) -> \
            SubMenuSchema:
        updated_submenu = await submenu_repository.update_submenu_by_id(menu_id, submenu_id, submenu_data, session)

        if not updated_submenu:
            raise HTTPException(status_code=404, detail='menu not found')

        return SubMenuSchema(
            id=str(updated_submenu.id),
            title=updated_submenu.title,
            description=updated_submenu.description,
            menu_id=str(updated_submenu.menu_id)
        )

    @staticmethod
    async def delete_submenu(submenu_id: str, session: AsyncSession) -> SubMenuSchema:
        deleted_menu = await submenu_repository.delete_submenu(submenu_id, session)
        return SubMenuSchema(
            id=str(deleted_menu.id),
            title=deleted_menu.title,
            description=deleted_menu.description,
            menu_id=str(deleted_menu.menu_id)
        )
