from fastapi import HTTPException
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


async def check_not_cadastral_number(
    cadastral_number: str | None,
) -> None:
    """Проверка проекта по названию"""
    if cadastral_number is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Не найден кадастровый номер!',
        )