from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime


class FundCommon:
    """Содержит общие поля моделей, относящихся к логике фонда."""
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, nullable=True)
