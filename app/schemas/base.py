from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CommonRetrieve(BaseModel):
    id: int
    full_amount: int = Field(..., le=1)
    create_date: datetime

    class Config:
        orm_mode = True


class CommonRetrieveExtended(CommonRetrieve):
    invested_amount: int = Field(..., le=0)
    fully_invested: bool
    close_date: Optional[datetime] = None
