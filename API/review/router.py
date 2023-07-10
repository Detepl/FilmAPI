from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi_users import FastAPIUsers

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import auth_backend
from auth.manager import get_user_manager
from database import get_async_session, User

from models.models import review, film
from review.schemas import ReviewPage, Review, ReviewCreate

router = APIRouter(
    tags=["Review"]
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

@router.get("/film/{id}/review/", response_model=ReviewPage)
async def get_reviews(id: int, session: AsyncSession = Depends(get_async_session), user=Depends(current_user)):
    query = select(review).where(review.c.film_id == id)
    result = await session.execute(query)
    return ReviewPage(data=[Review.from_orm(obj) for obj in result.all()])


@router.post("/film/review/")
async def add_review(new_review: ReviewCreate, session: AsyncSession = Depends(get_async_session), user=Depends(current_user)):
    film_exist = await session.execute(select(film).where(film.c.id == new_review.film_id)).all()
    if not film_exist:
        raise HTTPException(status_code=404, detail="film doesnt exists")

    stmt = insert(review).values(**new_review.dict())
    await session.execute(stmt)
    await session.commit()
    return new_review.dict()
