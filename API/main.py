from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from review.router import router as router_review
from film.router import router as router_film


app = FastAPI(
    title="Test"
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"]
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)


app.include_router(router_review)
app.include_router(router_film)
