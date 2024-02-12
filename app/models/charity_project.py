from sqlalchemy import Column, String, Text

from app.core.config import SYMBOL_MAX_LENGTH
from app.models.base import CharityDonationBase


class CharityProject(CharityDonationBase):
    name = Column(String(SYMBOL_MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text(), nullable=False)

    def __repr__(self):
        return (
            f'Проект {self.name}: {self.description}'
        )