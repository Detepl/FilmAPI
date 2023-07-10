import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FilmCreate(BaseModel):
    name: str
    genre: str
    short_description: str = Field(max_length=150)
    full_description: str
    date: datetime.date


class FilmAll(BaseModel):
    id: int
    name: str
    genre: str
    short_description: str

    class Config:
        orm_mode = True


class Film(BaseModel):
    name: str
    genre: str
    short_description: str
    full_description: str
    date: datetime.date
    avg_review: Optional[float]

    class Config:
        orm_mode = True




