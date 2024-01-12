from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.crud import CharityProjectCRUD, DonationCRUD
from .base import ServiceBase


class DonationService(ServiceBase):
    def __init__(self):
        super().__init__(DonationCRUD(), CharityProjectCRUD())

    async def get_all_by_user(
        self,
        session: AsyncSession,
        user: models.User,
    ) -> list[models.Donation]:
        donations = await self.main_crud.get_all_by_user(session, user)
        return donations
