from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.crud import BaseCRUD


async def require_investment(
    required_amount: int, session: AsyncSession
) -> int:
    """Запрашивает требуемую сумму инвестиций из пожертвований.
    Возвращает предоставленную пожертвованиями сумму инестиций.
    """
    return await _do_transfers(models.Donation, required_amount, session)


async def distribute_investment(
    full_amount: int, session: AsyncSession
) -> int:
    """Направляет имеющуюся сумму инвестиций в проекты.
    Возвращает принятую проектами сумму инестиций.
    """
    return await _do_transfers(models.CharityProject, full_amount, session)


async def _do_transfers(
    model, full_amount: int, session: AsyncSession
) -> int:
    """Перемещает заданное количество средств из открытых пожертвований
    или в открытые проекты (задаётся параметром model).
    Возвращает реально перемещённое количество средств.
    """
    assert full_amount > 0
    transferred_amount = 0
    objs = await BaseCRUD(model).get_all_opened(session)
    for obj in objs:
        transferred_amount += _transfer_money(
            obj, full_amount - transferred_amount
        )
        session.add(obj)
        if transferred_amount >= full_amount:
            break

    return transferred_amount


def _transfer_money(
    obj: Union[models.Donation, models.CharityProject],
    required_amount: int
) -> int:
    """Забирает заданное количество средств из открытого пожертвования
    или помещает заданное количество средств в открытый проект
    (задаётся параметром obj).
    Возвращает реально перемещённое количество средств.
    """
    assert required_amount > 0
    assert not obj.fully_invested
    rest_amount = obj.full_amount - obj.invested_amount
    assert rest_amount > 0
    if required_amount >= rest_amount:
        obj.invested_amount = obj.full_amount
        obj.fully_invested = True
        obj.close_date = datetime.now()
        return rest_amount

    obj.invested_amount += required_amount
    return required_amount
