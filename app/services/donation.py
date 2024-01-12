from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.crud import CharityProjectCRUD, DonationCRUD
from .base import ServiceBase


class DonationService(ServiceBase):
    def __init__(self):
        super().__init__(DonationCRUD(), CharityProjectCRUD())

    async def create(
        self,
        obj_in: schemas.DonationCreateInput,
        session: AsyncSession,
        user: models.User
    ) -> models.Donation:
        invested_amount = await self.do_transfers(
            self.aux_crud, obj_in.full_amount, session
        )
        donation = await self.main_crud.create(
            obj_in, invested_amount, session, user
        )
        return donation

    async def get_all_by_user(
        self,
        session: AsyncSession,
        user: models.User,
    ) -> list[models.Donation]:
        donations = await self.main_crud.get_all_by_user(session, user)
        return donations
