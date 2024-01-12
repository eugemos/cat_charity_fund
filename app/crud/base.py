from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models


class BaseCRUD:
    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_all(
        self,
        session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def get_all_opened(
        self,
        session: AsyncSession,
    ) -> list[models.Donation]:
        db_objs = await session.execute(
            select(self.model).where(
                self.model.fully_invested == False  # noqa
            )
        )
        return db_objs.scalars().all()

    async def create(
        self,
        data: dict,
        session: AsyncSession,
    ):
        db_obj = self.model(**data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
