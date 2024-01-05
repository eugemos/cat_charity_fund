from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.crud import DonationCRUD, CharityProjectCRUD


async def require_investment(
    required_amount: int, session: AsyncSession
) -> int:
    assert required_amount > 0
    received_amount = 0
    donations = await DonationCRUD().get_all_opened(session)
    for donation in donations:
        received_amount += get_money(
            donation, required_amount - received_amount
        )
        session.add(donation)
        if received_amount >= required_amount:
            break

    return received_amount


async def distribute_investment(
    full_amount: int, session: AsyncSession
) -> int:
    assert full_amount > 0
    distributed_amount = 0

    charity_projects = await CharityProjectCRUD().get_all_opened(session)
    for charity_project in charity_projects:
        distributed_amount += put_money(
            charity_project, full_amount - distributed_amount
        )
        session.add(charity_project)
        if distributed_amount >= full_amount:
            break

    return distributed_amount


def get_money(donation: models.Donation, required_amount: int):
    assert required_amount > 0
    assert not donation.fully_invested
    free_amount = donation.full_amount - donation.invested_amount
    assert free_amount > 0
    if required_amount >= free_amount:
        donation.invested_amount = donation.full_amount
        donation.fully_invested = True
        donation.close_date = datetime.now()
        return free_amount

    donation.invested_amount += required_amount
    return required_amount


def put_money(charity_project: models.CharityProject, required_amount: int):
    assert required_amount > 0
    assert not charity_project.fully_invested
    free_amount = charity_project.full_amount - charity_project.invested_amount
    assert free_amount > 0
    if required_amount >= free_amount:
        charity_project.invested_amount = charity_project.full_amount
        charity_project.fully_invested = True
        charity_project.close_date = datetime.now()
        return free_amount

    charity_project.invested_amount += required_amount
    return required_amount
