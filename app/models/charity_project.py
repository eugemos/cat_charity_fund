from sqlalchemy import Column, String, Text

from app.core.db import Base
from .common import FundCommon


class CharityProject(Base, FundCommon):
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
