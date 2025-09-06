from app.models import History
from sqlalchemy import select, literal
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from sqlalchemy.orm import joinedload


class HistoryCrud(CRUDBase):

    async def get_cadastral_number(
        self,
        cadastral_id: int,
        session: AsyncSession,
    ):
        """ПОлучить историю по кадастровому номеру."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.request_id == cadastral_id
            )
            .options(joinedload(self.model.request))
        )
        return db_obj.scalars().all()


history_crud = HistoryCrud(History)
