from typing import Optional

from pydantic import BaseModel, Field

from .base import CommonRetrieve, CommonRetrieveExtended


class DonationRetrieve(CommonRetrieveExtended):
    comment: Optional[str] = None
    user_id: int


class DonationCreate(BaseModel):
    full_amount: int = Field(..., le=1)
    comment: Optional[str] = None


class DonationRetrieveMy(CommonRetrieve):
    comment: Optional[str] = None
