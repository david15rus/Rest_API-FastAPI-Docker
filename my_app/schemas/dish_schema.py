from pydantic import BaseModel


class DishSchema(BaseModel):
    id: str
    title: str
    description: str
    price: str
    submenu_id: str
    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': 'c3350036-0df5-42bf-994c-56cb053f513d',
                    'title': 'Nice Dish',
                    'description': 'A very nice Dish',
                    'submenu_id': '37701f9f-0c6b-4d87-9696-1637a1cc0c7f',
                    'price': '325.12',
                }
            ]
        }
    }


class DishSchemaAdd(BaseModel):
    id: str | None = None
    title: str
    description: str
    price: str


class DishSchemaUpdate(BaseModel):
    title: str
    description: str
    price: str
