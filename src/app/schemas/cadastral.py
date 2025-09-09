from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CadastralDB(BaseModel):
    """Вывод информации о запросе"""
    id: int
    cadastral_number: str
    latitude: float
    longitude: float
    # result: Optional[bool]

    class Config:
        from_attributes = True


class CadastralCreate(BaseModel):
    """Добавление"""
    cadastral_number: str = Field(..., min_length=1, max_length=50)
    latitude: float = Field(...)
    longitude: float = Field(...)


class ResponseServer(BaseModel):
    """Ответ эмулируемого сервера"""
    status: bool


class CadastralCheck(BaseModel):
    """Ответ эмулируемого сервера"""
    request_id: str = Field(..., description="ID записи из RequestModel")
    status: Optional[bool] = Field(None, description="Результат запроса")


class HistoryDB(BaseModel):
    """Вывод информации о запросе"""
    created_at: datetime
    request_id: int
    status: Optional[bool]
    # cadastral_number: str

    class Config:
        from_attributes = True
