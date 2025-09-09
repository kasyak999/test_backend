from fastapi import FastAPI, Depends

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session, engine
from app.api.routers import main_router

from sqladmin import Admin
from app.core.admin import (
    UserAdmin, RequestModelAdmin, HistoryAdmin, AdminAuth)
from app.core.config import settings

app = FastAPI()

app.include_router(main_router)


authentication_backend = AdminAuth(secret_key=settings.secret)
admin = Admin(app, engine, authentication_backend=authentication_backend)
# admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(RequestModelAdmin)
admin.add_view(HistoryAdmin)


@app.get(
    '/ping_db',
    summary='Проверка подключения к базе данных',
    description=(
        'Этот эндпоинт выполняет простой SQL-запрос `SELECT 1`, '
        'чтобы убедиться, что соединение с базой данных установлено.'
    ),
    response_description='Статус соединения и результат запроса',
)
async def ping_db(
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Проверка подключения к базе данных."""
    try:
        result = await session.execute(text('SELECT 1'))
        return {'status': 'ok', 'result': result.scalar()}
    except SQLAlchemyError as e:
        return {'status': 'ошибка', 'detail': str(e)}
