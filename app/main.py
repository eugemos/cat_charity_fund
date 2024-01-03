from fastapi import FastAPI

# from app.api.routers import main_router
from app.core.config import settings
# from app.core.init_db import create_first_superuser


app = FastAPI(
    title=settings.app_title,
    description=f'{settings.description}<br/>Разработчик: {settings.app_author}'
)

# app.include_router(main_router)


# При старте приложения запускаем корутину create_first_superuser.
# @app.on_event('startup')
# async def startup():
#     await create_first_superuser()
