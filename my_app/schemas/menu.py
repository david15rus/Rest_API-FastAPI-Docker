from pydantic import BaseModel


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
                    'title': 'Nice item',
                    'description': 'A very nice Item',
                    'submenus_count': 3,
                    'dishes_count': 35,
                }
            ]
        }
    }


class MenuSchemaAdd(BaseModel):
    title: str
    description: str


class MenuSchemaUpdate(BaseModel):
    title: str
    description: str
