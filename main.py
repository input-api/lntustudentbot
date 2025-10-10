import asyncio
import os

from aiogram import Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats, Message
from aiogram.filters import Command

from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from sqlalchemy.ext.asyncio import AsyncSession

import logging

from bot import bot
from db.orm_query import orm_get_user_data, orm_update_user_data, orm_add_user_data, orm_get_users_data, \
    orm_add_to_white_list
from filters.main_filters import IsAdmin
from kbds.user.main_kbd import main_keyboard
from routers.admin_router import admin_router
from routers.superadmin_router import super_admin_router

logging.basicConfig(level=logging.INFO)
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from db.engine import create_db, session_maker, drop_db
from routers.user_router import user_router
from common.bot_cmds_list import user_cmd, admin_cmd
from middlewares.db import DataBaseMiddleware
from data.config import SUDO, WEBHOOK_ADDRESS, WEBHOOK_LISTENING_HOST, WEBHOOK_LISTENING_PORT, WEBHOOK_PATH

dp = Dispatcher()

dp.include_router(user_router)
dp.include_router(admin_router)
dp.include_router(super_admin_router)


async def on_startup(bot):
    await create_db()
    await bot.set_webhook(WEBHOOK_ADDRESS + WEBHOOK_PATH)

async def on_shutdown(bot):
    await bot.delete_webhook()
    await bot.session.close() 
    # await drop_db()


@dp.message(Command("updsudo"))
async def process(message: Message, session: AsyncSession):
    sudo_id = SUDO
    if sudo_id:
        await orm_add_to_white_list(session, id=sudo_id)
        await message.answer("Суперадміністратора додано")
    else:
        await message.answer("Не знайдено значення SUDO у змінних оточення.")

@dp.message(Command("start"), IsAdmin())
async def start_with_admin(message: Message, session: AsyncSession):
    await check_user_in_db(message, session)
    await orm_get_users_data(session)
    await bot.set_my_commands(commands=admin_cmd, scope=BotCommandScopeAllPrivateChats())
    await message.answer("Привіііт."
                         f"\nЯ бот-помічник студента ЛНТУ."
                         f"\nОсь що я можу запропонувати:", reply_markup=main_keyboard())

@dp.message(Command("start"), ~IsAdmin())
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

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseMiddleware(session_pool=session_maker))

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=WEBHOOK_LISTENING_HOST, port=WEBHOOK_LISTENING_PORT)
    await site.start()

    print("Bot is running via webhook...")

    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        print("🛑 Server stopped by user (Ctrl+C)")

if __name__ == "__main__":
    asyncio.run(main())