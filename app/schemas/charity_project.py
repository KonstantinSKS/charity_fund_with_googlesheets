from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator, PositiveInt

from app.core.config import SYMBOL_MAX_LENGTH, SYMBOL_MIN_LENGTH


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=SYMBOL_MIN_LENGTH,
                                max_length=SYMBOL_MAX_LENGTH)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=SYMBOL_MIN_LENGTH,
                      max_length=SYMBOL_MAX_LENGTH)
    description: str = Field(..., min_length=SYMBOL_MIN_LENGTH)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    @validator('name', 'description')
    def name_description_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError('Значение не должно быть пустым!')
        return value

    @validator('full_amount')
    def full_amount_cant_be_null(cls, value: int):
        if value is None or not isinstance(value, int):
            raise ValueError('Сумма проекта не может быть пустой!')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
