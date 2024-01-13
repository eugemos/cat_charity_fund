from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.core.constants import MAX_NAME_LENGTH
from .mixins import CommonFundFieldsMixin


class CharityProject(Base, CommonFundFieldsMixin):
    name = Column(String(MAX_NAME_LENGTH), nullable=False)
    description = Column(Text, nullable=False)
