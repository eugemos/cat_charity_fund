from typing import Optional

from pydantic import BaseModel, Field

from .base import CommonOutputExtended


class CharityProjectGeneralOutput(CommonOutputExtended):
    """Выходная модель для всех типов запросов."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)


class CharityProjectInputRequired(BaseModel):
    """Входная модель с обязательными полями."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., ge=1)


class CharityProjectInputOptional(BaseModel):
    """Входная модель с опциональными полями."""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    full_amount: int = Field(None, ge=1)


class CharityProjectCreateInput(CharityProjectInputRequired):
    """Входная модель для создания."""
    pass


class CharityProjectUpdateInput(CharityProjectInputOptional):
    """Входная модель для обновления."""
    pass
