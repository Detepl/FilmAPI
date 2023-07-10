from typing import List

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    film_id: int
    comment: str
    grade: int = Field(..., gt=0, lt=6)


class Review(BaseModel):
    film_id: int
    comment: str
    grade: int

    class Config:
        orm_mode = True


class ReviewPage(BaseModel):
    data: List[Review] = []