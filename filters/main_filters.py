from aiogram.filters import Filter
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import Position, WhiteList


class IsAdmin(Filter):
    def __init__(self) -> None:
        self.admin_list = []

    async def load_admins(self, session: AsyncSession):
        async with session:
            result = await session.execute(select(Position.tg_id).where(Position.is_admin == True))
            self.admin_list = result.scalars().all()
            print(self.admin_list)

    async def __call__(self, message: types.Message, session: AsyncSession) -> bool:
        await self.load_admins(session)
        return message.from_user.id in self.admin_list

class IsSuperAdmin(Filter):
    def __init__(self) -> None:
        self.super_admin_list = []

    async def load_super_admins(self, session: AsyncSession):
        async with session:
            result = await session.execute(select(WhiteList.superadmin_id))
            self.super_admin_list = result.scalars().all()

    async def __call__(self, message: types.Message, session: AsyncSession) -> bool:
        if not self.super_admin_list:
            await self.load_super_admins(session)
        return message.from_user.id in self.super_admin_list