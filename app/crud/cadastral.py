from app.models import RequestModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase


class CadastralCrud(CRUDBase):

    async def get_id(
        self,
        cadastral_number: str,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model.id).where(
                self.model.cadastral_number == cadastral_number
            )
        )
        # return db_obj.scalars().first()
        return db_obj.scalar_one_or_none()


cadastral_crud = CadastralCrud(RequestModel)
