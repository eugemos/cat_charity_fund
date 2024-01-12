from datetime import datetime
from typing import Union, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.crud import BaseCRUD


class ServiceBase:
    def __init__(self, main_crud: BaseCRUD, aux_crud: BaseCRUD):
        self.main_crud = main_crud
        self.aux_crud = aux_crud

    async def get_all(
        self, session: AsyncSession
    ) -> list[Union[models.Donation, models.CharityProject]]:
        objs = await self.main_crud.get_all(session)
        return objs

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[models.User] = None,
    ) -> Union[models.Donation, models.CharityProject]:
        invested_amount = await self._do_transfers(
            self.aux_crud, obj_in.full_amount, session
        )
        creation_data = self._prepare_data_for_creation(
            obj_in, invested_amount, user
        )
        db_obj = await self.main_crud.create(
            creation_data, session
        )
        return db_obj

    def _prepare_data_for_creation(
        self,
        obj_in,
        invested_amount: int,
        user: Optional[models.User] = None,
    ) -> dict:
        data = obj_in.dict()
        data['invested_amount'] = invested_amount
        if invested_amount >= obj_in.full_amount:
            data['fully_invested'] = True
            data['close_date'] = datetime.now()

        if user is not None:
            data['user_id'] = user.id

        return data

    async def _do_transfers(
        self, crud: BaseCRUD, full_amount: int, session: AsyncSession
    ) -> int:
        """Перемещает заданное количество средств из открытых пожертвований
        или в открытые проекты (зависит от crud).
        Возвращает реально перемещённое количество средств.
        """
        assert full_amount > 0
        transferred_amount = 0
        objs = await crud.get_all_opened(session)
        for obj in objs:
            transferred_amount += self._transfer_money(
                obj, full_amount - transferred_amount
            )
            session.add(obj)
            if transferred_amount >= full_amount:
                break

        return transferred_amount

    def _transfer_money(
        self,
        obj: Union[models.Donation, models.CharityProject],
        required_amount: int
    ) -> int:
        """Забирает заданное количество средств из открытого пожертвования
        или помещает заданное количество средств в открытый проект
        (зависит от типа obj).
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
