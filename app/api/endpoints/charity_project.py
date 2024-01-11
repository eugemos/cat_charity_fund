from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.services import CharityProjectService

service = CharityProjectService()

router = APIRouter()


@router.post(
    '/',
    response_model=schemas.CharityProjectGeneralOutput,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    obj_in: schemas.CharityProjectCreateInput,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперпользователей."""
    charity_project = await service.create(obj_in, session)
    return charity_project


@router.get(
    '/',
    response_model=list[schemas.CharityProjectGeneralOutput],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Доступно всем."""
    charity_projects = await service.get_all(session)
    return charity_projects


@router.patch(
    '/{charity_project_id}',
    response_model=schemas.CharityProjectGeneralOutput,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    charity_project_id: int,
    obj_in: schemas.CharityProjectUpdateInput,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперпользователей."""
    charity_project = await service.update(
        charity_project_id, obj_in, session
    )
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=schemas.CharityProjectGeneralOutput,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперпользователей."""
    charity_project = await service.delete(charity_project_id, session)
    return charity_project
