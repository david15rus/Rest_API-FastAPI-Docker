from pydantic import BaseModel

from my_app.schemas.submenu import SubMenuSchemaWithDish


class MenuSchema(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int | None = 0
    dishes_count: int | None = 0
    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '8c9d7526-c5cb-4adf-8862-a76f649891e9',
                    'title': 'Nice Menu',
                    'description': 'A very nice Menu',
                    'submenus_count': 3,
                    'dishes_count': 35,
                }
            ]
        }
    }


class MenuSchemaWithAll(BaseModel):
    id: str
    title: str
    description: str
    submenus: list[SubMenuSchemaWithDish]


class MenuSchemaAdd(BaseModel):
    id: str | None = None
    title: str
    description: str


class MenuSchemaUpdate(BaseModel):
    title: str
    description: str
