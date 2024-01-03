from sqlalchemy import Column, String, Text

from .base import FundBase


class CharityProject(FundBase):
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
