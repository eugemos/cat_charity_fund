from datetime import datetime
from typing import Optional

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

    async def create(
            self,
            obj_in,
            invested_amount: int,
            session: AsyncSession,
            user: Optional[models.User] = None,
    ):
        obj_in_data = obj_in.dict()
        obj_in_data['invested_amount'] = invested_amount
        if invested_amount >= obj_in.full_amount:
            obj_in_data['fully_invested'] = True
            obj_in_data['close_date'] = datetime.now()

        if user is not None:
            obj_in_data['user_id'] = user.id

        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        # print(f'*************\n{obj_in=}\n{obj_in_data=}\n{db_obj=}\n**************')
        return db_obj
