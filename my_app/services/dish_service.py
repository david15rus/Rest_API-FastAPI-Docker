from fastapi import HTTPException
from my_app.repositories import dish_repository
from my_app.schemas.dish import DishSchema, DishSchemaAdd, DishSchemaUpdate


class DishService:
    @staticmethod
    async def create_dish(submenu_id: str, dish_data: DishSchemaAdd, session):
        new_dish = await dish_repository.create_dish(submenu_id, dish_data, session)

        return new_dish

    @staticmethod
    async def read_dishes(submenu_id: str, skip: int, limit: int, session):
        dishes = await dish_repository.get_all_dishes(submenu_id, skip, limit, session)

        response_data = []
        for dish in dishes:
            response_data.append(
                {
                    "id": str(dish.id),
                    "title": dish.title,
                    "description": dish.description,
                    "price": str(round(dish.price, 2)),
                }
            )
        return response_data

    @staticmethod
    async def read_one_dish(submenu_id: str, dish_id: str, session):
        dish = await dish_repository.get_submenu_by_id(submenu_id, dish_id, session)

        if not dish:
            raise HTTPException(status_code=404, detail="dish not found")

        response_data = {
            "id": str(dish.id),
            "title": dish.title,
            "description": dish.description,
            "price": str(round(dish.price, 2)),
        }
        return response_data

    @staticmethod
    async def update_dish(submenu_id: str, dish_id: str, dish_data: DishSchemaUpdate, session):
        updated_dish = await dish_repository.update_dish_by_id(submenu_id, dish_id, dish_data, session)

        if not updated_dish:
            raise HTTPException(status_code=404, detail="menu not found")

        response_data = {
            "id": str(updated_dish.id),
            "title": updated_dish.title,
            "description": updated_dish.description,
            "price": str(round(updated_dish.price, 2)),
        }
        return response_data

    @staticmethod
    async def delete_dish(submenu_id: str, dish_id: str, session):
        deleted_dish = await dish_repository.delete_dish(submenu_id, dish_id, session)
        return deleted_dish
