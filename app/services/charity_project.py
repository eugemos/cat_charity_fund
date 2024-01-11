from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from .base import ServiceBase
from .validators import (
    check_charity_project_exists,
    check_charity_project_name_unique,
    check_charity_project_may_be_deleted,
    check_charity_project_may_be_updated,
)


class CharityProjectService(ServiceBase):
    async def create(
        self,
        obj_in: schemas.CharityProjectCreateInput,
        session: AsyncSession
    ) -> models.CharityProject:
        await check_charity_project_name_unique(obj_in.name, session)
        invested_amount = await self._require_investment(
            obj_in.full_amount, session
        )
        charity_project = await self.charity_project_crud.create(
            obj_in, invested_amount, session
        )
        return charity_project

    async def get_all(
        self, session: AsyncSession
    ) -> list[models.CharityProject]:
        charity_projects = await self.charity_project_crud.get_all(session)
        return charity_projects

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

        charity_project = await self.charity_project_crud.update(
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
        charity_project = await self.charity_project_crud.remove(
            charity_project, session
        )
        return charity_project

    async def _require_investment(
        self, required_amount: int, session: AsyncSession
    ) -> int:
        """Запрашивает требуемую сумму инвестиций из пожертвований.
        Возвращает предоставленную пожертвованиями сумму инестиций.
        """
        return await self.do_transfers(
            self.donation_crud, required_amount, session
        )
