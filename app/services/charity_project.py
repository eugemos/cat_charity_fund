from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.crud import CharityProjectCRUD, DonationCRUD
from .base import ServiceBase
from .validators import (
    check_charity_project_exists,
    check_charity_project_name_unique,
    check_charity_project_may_be_deleted,
    check_charity_project_may_be_updated,
)


class CharityProjectService(ServiceBase):
    def __init__(self):
        super().__init__(CharityProjectCRUD(), DonationCRUD())

    async def create(
        self,
        obj_in: schemas.CharityProjectCreateInput,
        session: AsyncSession
    ) -> models.CharityProject:
        await check_charity_project_name_unique(obj_in.name, session)
        invested_amount = await self.do_transfers(
            self.aux_crud, obj_in.full_amount, session
        )
        charity_project = await self.main_crud.create(
            obj_in, invested_amount, session
        )
        return charity_project

    async def update(
        self,
        charity_project_id: int,
        obj_in: schemas.CharityProjectUpdateInput,
        session: AsyncSession,
    ) -> models.CharityProject:
        charity_project = await check_charity_project_exists(
            charity_project_id, session
        )
        check_charity_project_may_be_updated(charity_project, obj_in)
        if obj_in.name is not None and obj_in.name != charity_project.name:
            await check_charity_project_name_unique(obj_in.name, session)

        charity_project = await self.main_crud.update(
            charity_project, obj_in, session
        )
        return charity_project

    async def delete(
        self,
        charity_project_id: int,
        session: AsyncSession,
    ) -> models.CharityProject:
        charity_project = await check_charity_project_exists(
            charity_project_id, session
        )
        check_charity_project_may_be_deleted(charity_project)
        charity_project = await self.main_crud.remove(
            charity_project, session
        )
        return charity_project
