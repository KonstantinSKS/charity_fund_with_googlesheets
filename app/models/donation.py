from sqlalchemy import Column, Integer, ForeignKey, Text

from app.models.base import CharityDonationBase


class Donation(CharityDonationBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Пожертвование {self.full_amount}: Комментарий {self.comment}'
        )
