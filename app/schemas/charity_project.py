from typing import Optional

from pydantic import BaseModel, Field

from core.constants import (
    MIN_FULL_AMOUNT, MIN_DESCRIPTION_LENGTH,
    MIN_NAME_LENGTH, MAX_NAME_LENGTH
)
from .base import CommonOutputExtended


class CharityProjectGeneralOutput(CommonOutputExtended):
    """Выходная модель для всех типов запросов."""
    name: str = Field(
        min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH
    )
    description: str = Field(min_length=MIN_DESCRIPTION_LENGTH)


class CharityProjectInputRequired(BaseModel):
    """Входная модель с обязательными полями."""
    name: str = Field(
        min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH
    )
    description: str = Field(min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: int = Field(ge=MIN_FULL_AMOUNT)


class CharityProjectInputOptional(BaseModel):
    """Входная модель с опциональными полями."""
    name: Optional[str] = Field(
        None, min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH
    )
    description: Optional[str] = Field(
        None, min_length=MIN_DESCRIPTION_LENGTH
    )
    full_amount: int = Field(None, ge=MIN_FULL_AMOUNT)

    class Config:
        extra = 'forbid'


class CharityProjectCreateInput(CharityProjectInputRequired):
    """Входная модель для создания."""
    pass


class CharityProjectUpdateInput(CharityProjectInputOptional):
    """Входная модель для обновления."""
    pass
