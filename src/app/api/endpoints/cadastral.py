
from fastapi import APIRouter, Depends
from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cadastral import (
    CadastralCreate, CadastralDB, ResponseServer, CadastralCheck, HistoryDB)
from app.crud.cadastral import cadastral_crud
from app.crud.history import history_crud
import time
from app.api.validators import (
    check_cadastral_number, check_not_cadastral_number)
from app.core.user import current_user
from app.models import User

router = APIRouter()


@router.post(
    '/query',
    response_model=CadastralDB,
    response_model_exclude_none=True,
    summary='Принимает кадастровый номер, широту и долготу'
)
async def create_donation(
    donation: CadastralCreate,
    dependencies: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Добавить кадастровый номер."""
    result = await cadastral_crud.get_id(donation.cadastral_number, session)
    await check_cadastral_number(result)
    return await cadastral_crud.create(donation, session)


@router.get(
    '/history',
    response_model=list[HistoryDB],
    response_model_exclude_none=True,
    summary='История запросов по кадастровому номеру.',
)
async def get_all_charity_projects(
    cadastral_number: str,
    session: AsyncSession = Depends(get_async_session),
):
    """История запросов."""
    cadastral_id = await cadastral_crud.get_id(cadastral_number, session)
    await check_not_cadastral_number(cadastral_id)
    return await history_crud.get_cadastral_number(cadastral_id, session)


@router.get(
    '/ping',
    response_model=ResponseServer,
    response_model_exclude_none=True,
    summary='Проверка, что сервер запустился',
)
async def get_all():
    """Тест сервера"""
    time.sleep(1)
    return ResponseServer(status=True)


@router.post(
    '/result',
    response_model=CadastralCheck,
    response_model_exclude_none=True,
    summary='Принимает кадастровый номер, широту и долготу'
)
async def check_cadastral(
    cadastral_number: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Проверка кадастрового номера."""
    response_server = {"status": True}  # Эмуляция ответа сервера
    cadastral_id = await cadastral_crud.get_id(cadastral_number, session)
    await check_not_cadastral_number(cadastral_id)
    cadastral = CadastralCheck(
        request_id=cadastral_id, status=response_server["status"])
    await history_crud.create(cadastral, session)
    return cadastral
