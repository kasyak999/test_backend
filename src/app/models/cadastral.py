from sqlalchemy import String, Float, Boolean, DateTime, func, ForeignKey
from app.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class RequestModel(Base):
    cadastral_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        comment='Кадастровый номер.',
    )
    latitude: Mapped[float] = mapped_column(
        Float(50),
        nullable=False,
        comment='Широта.',
    )
    longitude: Mapped[float] = mapped_column(
        Float(50),
        nullable=False,
        comment='Долгота.',
    )

    histories: Mapped[list["History"]] = relationship(
        back_populates="request",
        cascade="all, delete-orphan"
    )


class History(Base):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),   # ставится при создании записи
        nullable=False,
        comment="Дата и время создания записи.",
    )
    request_id: Mapped[int] = mapped_column(
        ForeignKey("requestmodel.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID Кадастровый номер.",
    )
    status: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True,
        comment='Результат запроса.',
    )

    request: Mapped["RequestModel"] = relationship(back_populates="histories")
