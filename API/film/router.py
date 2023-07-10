from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi_users import FastAPIUsers

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from auth.auth import auth_backend
from auth.manager import get_user_manager
from database import get_async_session, User
from film.schemas import FilmAll, Film, FilmCreate

from models.models import film, review

router = APIRouter(
    tags=["Film"]
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@router.get("/film/", response_model=List[FilmAll])
async def get_films(session: AsyncSession = Depends(get_async_session)):
    query = select(film)
    result = await session.execute(query)
    return [FilmAll.from_orm(obj) for obj in result.all()]


@router.get("/film/{id}", response_model=Film)
async def get_film(id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(film).where(film.c.id == id)
    part = await session.execute(query)
    data = part.all()
    if data:
        data = data[0]
        result = Film.from_orm(data)
    else:
        raise HTTPException(status_code=404, detail="film doesnt exists")

    avg_grade = select(func.avg(review.c.grade).label('average_grade')).select_from(review).where(review.c.film_id == id)
    part = await session.execute(avg_grade)
    result.avg_review = part.all()[0][0]

    return result


@router.post("/film/")
async def add_review(new_film: FilmCreate, session: AsyncSession = Depends(get_async_session),  user=Depends(current_user)):
    stmt = insert(film).values(**new_film.dict())
    await session.execute(stmt)
    await session.commit()
    return new_film.dict()
