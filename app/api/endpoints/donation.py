from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.services import DonationService as Service


router = APIRouter()


@router.post(
    '/',
    response_model=schemas.DonationCreateOutput,
    response_model_exclude_none=True,
)
async def create_donation(
    obj_in: schemas.DonationCreateInput,
    session: AsyncSession = Depends(get_async_session),
    user: models.User = Depends(current_user),
):
    """Только для зарегистрированных пользователей."""
    donation = await Service(session).create(obj_in, user)
    return donation


@router.get(
    '/',
    response_model=list[schemas.DonationListOutput],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперпользователей."""
    donations = await Service(session).get_all()
    return donations


@router.get(
    '/my',
    response_model=list[schemas.DonationListByUserOutput],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: models.User = Depends(current_user),
):
    """Только для зарегистрированных пользователей."""
    donations = await Service(session).get_all_by_user(user)
    return donations
