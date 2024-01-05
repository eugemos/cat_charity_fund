from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.crud import CharityProjectCRUD


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> models.CharityProject:
    charity_project = await CharityProjectCRUD().get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


def check_charity_project_may_be_deleted(
    charity_project: models.CharityProject
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Проект нельзя удалить: он закрыт!'
        )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Проект нельзя удалить: в него внесены средства!'
        )


def check_charity_project_may_be_updated(
    charity_project: models.CharityProject,
    obj_in: schemas.CharityProjectUpdateInput,
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Проект нельзя изменить: он закрыт!'
        )

    if (obj_in.full_amount is not None and
            charity_project.invested_amount > obj_in.full_amount):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить для проекта новую требуемую сумму, '
                   'которая меньше уже внесённой!'
        )
