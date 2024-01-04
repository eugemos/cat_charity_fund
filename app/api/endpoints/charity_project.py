from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import CharityProjectCRUD
from app import schemas

from app.api.validators import check_charity_project_exists
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
    charity_project = await CharityProjectCRUD().create(charity_project, session)
    return charity_project


@router.get(
    '/',
    response_model=list[schemas.CharityProjectGeneralOutput],
    response_model_exclude_none=True,
)
async def list_charity_project(
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
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: schemas.CharityProjectUpdateInput,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )

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
async def remove_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    charity_project = await CharityProjectCRUD().remove(charity_project, session)
    return charity_project
