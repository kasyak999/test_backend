from sqladmin import ModelView
from app.models import User, History, RequestModel
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from passlib.context import CryptContext
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import engine
from sqlalchemy import inspect


def get_column_comments(model):
    mapper = inspect(model)
    labels = {}
    for column in mapper.columns:
        if column.comment:
            labels[column.name] = column.comment
    return labels


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]


class RequestModelAdmin(ModelView, model=RequestModel):
    column_list = [RequestModel.id, RequestModel.cadastral_number]
    # name = "Request1"
    # name_plural = "Requests33"
    column_labels = get_column_comments(RequestModel)


class HistoryAdmin(ModelView, model=History):
    column_list = [
        History.id, History.request_id, History.created_at, History.status]
    column_labels = get_column_comments(History)


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, hashed_password = form["username"], form["password"]

        async with AsyncSession(engine) as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()

        if not user:
            return False
        if not pwd_context.verify(hashed_password, user.hashed_password):
            return False
        if not user.is_superuser:
            return False

        request.session.update({"user": user.email})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return "user" in request.session

