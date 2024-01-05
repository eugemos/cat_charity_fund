# from typing import Optional

from fastapi.encoders import jsonable_encoder
# from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from .base import BaseCRUD


class CharityProjectCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(models.CharityProject)

    async def create(
            self,
            obj_in: schemas.CharityProjectCreateInput,
            session: AsyncSession,
    ) -> models.CharityProject:
        return await super().create(obj_in, session)

    async def update(
            self,
            db_obj: models.CharityProject,
            obj_in: schemas.CharityProjectUpdateInput,
            session: AsyncSession,
    ) -> models.CharityProject:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        if db_obj.invested_amount >= db_obj.full_amount:
            db_obj.fully_invested = True

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: models.CharityProject,
        session: AsyncSession,
    ) -> models.CharityProject:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
