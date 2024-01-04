from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.crud import CharityProjectCRUD


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> models.CharityProject:
    charity_project = await CharityProjectCRUD().get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project
