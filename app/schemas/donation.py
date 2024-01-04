from typing import Optional

from pydantic import BaseModel, Field

from .base import CommonOutput, CommonOutputExtended


class DonationOutputFull(CommonOutputExtended):
    """Выходная модель с полным набором полей."""
    comment: Optional[str] = None
    user_id: int


class DonationOutputShortened(CommonOutput):
    """Выходная модель с сокращённым набором полей."""
    comment: Optional[str] = None


class DonationListOutput(DonationOutputFull):
    """Выходная модель для получения полного списка."""
    pass


class DonationListByUserOutput(DonationOutputShortened):
    """Выходная модель для получения пользовательского списка."""
    pass


class DonationCreateOutput(DonationOutputShortened):
    """Выходная модель для создания."""
    pass


class DonationCreateInput(BaseModel):
    """Входная модель для создания."""
    full_amount: int = Field(..., ge=1)
    comment: Optional[str] = None
