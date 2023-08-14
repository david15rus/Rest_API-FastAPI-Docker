from pydantic import BaseModel

from my_app.schemas.dish import DishSchema


class SubMenuSchema(BaseModel):
    id: str
    title: str
    description: str
    menu_id: str
    dishes_count: int | None = 0
    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '37701f9f-0c6b-4d87-9696-1637a1cc0c7f',
                    'title': 'Nice Submenu',
                    'description': 'A very nice Submenu',
                    'menu_id': '8c9d7526-c5cb-4adf-8862-a76f649891e9',
                    'dishes_count': 35,
                }
            ]
        }
    }


class SubMenuSchemaWithDish(BaseModel):
    id: str
    title: str
    description: str
    menu_id: str
    dishes: list[DishSchema]


class SubMenuSchemaAdd(BaseModel):
    id: str | None = None
    title: str
    description: str


class SubMenuSchemaUpdate(BaseModel):
    title: str
    description: str
