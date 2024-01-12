from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .constants import MIN_FULL_AMOUNT, MIN_INVESTED_AMOUNT


class CommonOutput(BaseModel):
    id: int
    full_amount: int = Field(ge=MIN_FULL_AMOUNT)
    create_date: datetime

    class Config:
        orm_mode = True


class CommonOutputExtended(CommonOutput):
    invested_amount: int = Field(ge=MIN_INVESTED_AMOUNT)
    fully_invested: bool
    close_date: Optional[datetime] = None
