from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from .base import ServiceBase


class DonationService(ServiceBase):
    async def create(
        self,
        donation: schemas.DonationCreateInput,
        session: AsyncSession,
        user: models.User
    ) -> models.Donation:
        invested_amount = await self._distribute_investment(
            donation.full_amount, session
        )
        donation = await self.donation_crud.create(
            donation, invested_amount, session, user
        )
        return donation

    async def get_all(
        self, session: AsyncSession
    ) -> list[models.Donation]:
        donations = await self.donation_crud.get_all(session)
        return donations

    async def get_all_by_user(
        self,
        session: AsyncSession,
        user: models.User,
    ) -> list[models.Donation]:
        donations = await self.donation_crud.get_all_by_user(session, user)
        return donations

    async def _distribute_investment(
        self, full_amount: int, session: AsyncSession
    ) -> int:
        """Направляет имеющуюся сумму инвестиций в проекты.
        Возвращает принятую проектами сумму инестиций.
        """
        return await self.do_transfers(
            self.charity_project_crud, full_amount, session
        )
