from sqlalchemy import Column, Integer, Text, ForeignKey

from .base import FundBase


class Donation(FundBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
