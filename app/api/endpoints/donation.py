from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import DonationCRUD
from app.services.investment import distribute_investment

# from app.api.validators import check_charity_project_exists
# check_name_duplicate,

router = APIRouter()


@router.post(
    '/',
    response_model=schemas.DonationCreateOutput,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: schemas.DonationCreateInput,
    session: AsyncSession = Depends(get_async_session),
    user: models.User = Depends(current_user),
):
    """Только для зарегистрированных пользователей."""
    invested_amount = await distribute_investment(donation.full_amount, session)
    donation = await DonationCRUD().create(
        donation, invested_amount, session, user
    )
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
    donations = await DonationCRUD().get_all(session)
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
    donations = await DonationCRUD().get_all_by_user(session, user)
    return donations
