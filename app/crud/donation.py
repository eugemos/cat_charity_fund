from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from .base import BaseCRUD


class DonationCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(models.Donation)

    async def create(
            self,
            obj_in: schemas.DonationCreateInput,
            invested_amount: int,
            session: AsyncSession,
            user: models.User,
    ) -> models.Donation:
        return await super().create(obj_in, invested_amount, session, user)

    async def get_all_by_user(
        self,
        session: AsyncSession,
        user: models.User,
    ) -> list[models.Donation]:
        db_objs = await session.execute(select(self.model).where(
            self.model.user_id == user.id
        ))
        return db_objs.scalars().all()
