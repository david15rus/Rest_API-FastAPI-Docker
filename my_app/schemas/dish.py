from pydantic import BaseModel


class DishSchema(BaseModel):
    id: str
    title: str
    description: str
    price: str
    submenu_id: str


class DishSchemaAdd(BaseModel):
    title: str
    description: str
    price: str


class DishSchemaUpdate(BaseModel):
    title: str
    description: str
    price: str
