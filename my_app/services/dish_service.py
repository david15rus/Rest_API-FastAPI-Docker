from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.repositories import dish_repository
from my_app.schemas.dish import DishSchema, DishSchemaAdd, DishSchemaUpdate


class DishService:
    @staticmethod
    async def create_dish(submenu_id: str, dish_data: DishSchemaAdd, session: AsyncSession) -> DishSchema:
        new_dish = await dish_repository.create_dish(submenu_id, dish_data, session)

        return DishSchema(
            id=str(new_dish.id),
            title=new_dish.title,
            description=new_dish.description,
            price=str(round(float(new_dish.price), 2)),
            submenu_id=str(new_dish.submenu_id)
        )

    @staticmethod
    async def read_dishes(submenu_id: str, skip: int, limit: int, session: AsyncSession) -> \
            list[DishSchema]:
        dishes = await dish_repository.get_all_dishes(submenu_id, skip, limit, session)

        response_data = []
        for dish in dishes:
            response_data.append(
                DishSchema(
                    id=str(dish.id),
                    title=dish.title,
                    description=dish.description,
                    price=str(round(float(dish.price), 2)),
                    submenu_id=str(dish.submenu_id)
                )
            )
        return response_data

    @staticmethod
    async def read_one_dish(submenu_id: str, dish_id: str, session: AsyncSession) -> DishSchema:
        dish = await dish_repository.get_submenu_by_id(submenu_id, dish_id, session)

        if not dish:
            raise HTTPException(status_code=404, detail='dish not found')

        return DishSchema(
            id=str(dish.id),
            title=dish.title,
            description=dish.description,
            price=str(round(float(dish.price), 2)),
            submenu_id=str(dish.submenu_id)
        )

    @staticmethod
    async def update_dish(submenu_id: str, dish_id: str, dish_data: DishSchemaUpdate, session: AsyncSession) -> \
            DishSchema:
        updated_dish = await dish_repository.update_dish_by_id(submenu_id, dish_id, dish_data, session)

        if not updated_dish:
            raise HTTPException(status_code=404, detail='menu not found')

        return DishSchema(
            id=str(updated_dish.id),
            title=updated_dish.title,
            description=updated_dish.description,
            price=str(round(float(updated_dish.price), 2)),
            submenu_id=str(updated_dish.submenu_id)
        )

    @staticmethod
    async def delete_dish(submenu_id: str, dish_id: str, session: AsyncSession) -> DishSchema:
        deleted_dish = await dish_repository.delete_dish(submenu_id, dish_id, session)
        return DishSchema(
            id=str(deleted_dish.id),
            title=deleted_dish.title,
            description=deleted_dish.description,
            price=str(round(float(deleted_dish.price), 2)),
            submenu_id=str(deleted_dish.submenu_id)
        )
