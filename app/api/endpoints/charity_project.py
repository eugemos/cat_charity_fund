from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import CharityProjectCRUD
from app.services.investment import require_investment

from app.api.validators import (
    check_charity_project_exists,
    check_charity_project_may_be_deleted,
    check_charity_project_may_be_updated,
)
# check_name_duplicate,

router = APIRouter()


@router.post(
    '/',
    response_model=schemas.CharityProjectGeneralOutput,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: schemas.CharityProjectCreateInput,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    invested_amount = await require_investment(
        charity_project.full_amount, session
    )
    charity_project = await CharityProjectCRUD().create(
        charity_project, invested_amount, session
    )
    return charity_project


@router.get(
    '/',
    response_model=list[schemas.CharityProjectGeneralOutput],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    charity_projects = await CharityProjectCRUD().get_all(session)
    return charity_projects


@router.patch(
    '/{charity_project_id}',
    response_model=schemas.CharityProjectGeneralOutput,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    charity_project_id: int,
    obj_in: schemas.CharityProjectUpdateInput,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    check_charity_project_may_be_updated(charity_project, obj_in)
    # if obj_in.name is not None:
    #     await check_name_duplicate(obj_in.name, session)

    charity_project = await CharityProjectCRUD().update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=schemas.CharityProjectGeneralOutput,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    check_charity_project_may_be_deleted(charity_project)
    charity_project = await CharityProjectCRUD().remove(charity_project, session)
    return charity_project
