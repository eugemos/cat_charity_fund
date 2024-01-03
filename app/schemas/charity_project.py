from typing import Optional

from pydantic import BaseModel, Field

from .base import CommonRetrieveExtended


class CharityProjectRetrieve(CommonRetrieveExtended):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)


class CharityProjectCreate(CommonRetrieveExtended):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., le=1)


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    full_amount: int = Field(None, le=1)
