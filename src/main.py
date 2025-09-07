from fastapi import FastAPI, Depends

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.api.routers import main_router
app = FastAPI()

app.include_router(main_router)


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
