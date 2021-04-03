from typing import Union

from pydantic import BaseModel, Field


class Interval(BaseModel):
    date_from: str = Field(alias="dateFrom")
    date_till: str = Field(alias="dateTill")


class Limit(BaseModel):
    currency: str
    rest: Union[float, int]
    max_limit: Union[float, int] = Field(alias="max")
    spent: Union[float, int]
    interval: Interval
    limit_type: str = Field(alias="type")


__all__ = [
    'Limit'
]
