from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base
from app.core.config import DEFAULT_INVESTED_AMOUNT


class CharityDonationBase(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False,
                             default=DEFAULT_INVESTED_AMOUNT)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
