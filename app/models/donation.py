from sqlalchemy import Column, Integer, Text, ForeignKey

from app.core.db import Base
from .mixins import CommonFundFieldsMixin


class Donation(Base, CommonFundFieldsMixin):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
