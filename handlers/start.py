from aiogram.types import BotCommandScopeAllPrivateChats, Message
from sqlalchemy.ext.asyncio import AsyncSession

from db.orm_query import orm_get_user_data, orm_update_user_data, orm_add_user_data, orm_get_users_data, \
    orm_add_to_white_list
from kbds.user.main_kbd import main_keyboard
from common.bot_cmds_list import user_cmd, admin_cmd
from data.config import SUDO
from bot import bot

async def process(message: Message, session: AsyncSession):
    if SUDO:
        await orm_add_to_white_list(session, id=SUDO)
        await message.answer("Суперадміністратора додано")
    else:
        await message.answer("Не знайдено значення SUDO у змінних оточення.")

async def start_with_admin(message: Message, session: AsyncSession):
    await check_user_in_db(message, session)
    await orm_get_users_data(session)
    await bot.set_my_commands(commands=admin_cmd, scope=BotCommandScopeAllPrivateChats())
    await message.answer("Привіііт."
                         f"\nЯ бот-помічник студента ЛНТУ."
                         f"\nОсь що я можу запропонувати:", reply_markup=main_keyboard())

async def start(message: Message, session: AsyncSession):
    await check_user_in_db(message, session)
    await orm_get_users_data(session)
    await bot.set_my_commands(commands=user_cmd, scope=BotCommandScopeAllPrivateChats())
    await message.answer("Привіііт."
                         f"\nЯ бот-помічник студента ЛНТУ."
                         f"\nОсь що я можу запропонувати:", reply_markup=main_keyboard())

async def check_user_in_db(message, session):
    data = {
        "tg_id": message.from_user.id,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "username": message.from_user.username
    }
    user = await orm_get_user_data(session, data["tg_id"])

    if user:
        await orm_update_user_data(session, data["tg_id"], data)
    else:
        await orm_add_user_data(session, data)