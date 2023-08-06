from pydantic import BaseModel


class SubMenuSchema(BaseModel):
    id: str
    title: str
    description: str
    menu_id: str
    dishes_count: int | None = 0


class SubMenuSchemaAdd(BaseModel):
    title: str
    description: str


class SubMenuSchemaUpdate(BaseModel):
    title: str
    description: str
