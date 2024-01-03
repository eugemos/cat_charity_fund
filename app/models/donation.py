from sqlalchemy import Column, Integer, Text, ForeignKey

from app.core.db import Base
from .common import FundCommon


class Donation(Base, FundCommon):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
