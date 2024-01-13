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
    def __init__(self, session: AsyncSession):
        super().__init__(CharityProjectCRUD(), DonationCRUD(), session)

    async def create(
        self,
        obj_in: schemas.CharityProjectCreateInput,
    ) -> models.CharityProject:
        await check_charity_project_name_unique(obj_in.name, self.session)
        charity_project = await super().create(obj_in)
        return charity_project

    async def update(
        self,
        charity_project_id: int,
        obj_in: schemas.CharityProjectUpdateInput,
    ) -> models.CharityProject:
        charity_project = await check_charity_project_exists(
            charity_project_id, self.session
        )
        check_charity_project_may_be_updated(charity_project, obj_in)
        if obj_in.name is not None and obj_in.name != charity_project.name:
            await check_charity_project_name_unique(obj_in.name, self.session)

        charity_project = await self.main_crud.update(
            charity_project, obj_in, self.session
        )
        return charity_project

    async def delete(
        self,
        charity_project_id: int,
    ) -> models.CharityProject:
        charity_project = await check_charity_project_exists(
            charity_project_id, self.session
        )
        check_charity_project_may_be_deleted(charity_project)
        charity_project = await self.main_crud.remove(
            charity_project, self.session
        )
        return charity_project
