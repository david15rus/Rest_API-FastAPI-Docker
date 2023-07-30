from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from my_app.config import get_session
from my_app.endpoints import menu, submenu, dish

app = FastAPI()

app.include_router(menu.router, prefix="/api/v1/menus", tags=["Menus"])
app.include_router(submenu.router, prefix="/api/v1/menus/{menu_id}/submenus", tags=["Submenus"])
app.include_router(dish.router, prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", tags=["Dishes"])


# Dependency to provide the database session
@app.middleware("http")
async def db_session_middleware(request, call_next, session: AsyncSession = Depends(get_session)):
    request.state.db = session
    response = await call_next(request)
    return response
