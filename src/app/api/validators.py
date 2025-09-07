from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
# from app.crud.charity_project import charity_project_crud
from app.models import RequestModel
from http import HTTPStatus


async def check_cadastral_number(
    cadastral_number: str | None,
) -> None:
    """Проверка проекта по названию"""
    if cadastral_number is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Уже существует!',
        )
