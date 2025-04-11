import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import handlers
from bot import bot
from data.config import (
    WEBHOOK_ADDRESS,
    WEBHOOK_PATH,
    WEBHOOK_LISTENING_HOST,
    WEBHOOK_LISTENING_PORT,
    WEBHOOK_SECRET_TOKEN,
)
from db.engine import create_db, session_maker
from middlewares.db import DataBaseMiddleware
from routers.user_router import user_router
from routers.admin_router import admin_router
from routers.superadmin_router import super_admin_router

def setup_handlers(dp: Dispatcher) -> None:
    handlers.prepare_router(dp)

def setup_aiogram(dp: Dispatcher) -> None:
    print("Configuring aiogram")
    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.include_router(super_admin_router)
    dp.update.middleware(DataBaseMiddleware(session_pool=session_maker))
    setup_handlers(dp)
    print("Configured aiogram")

async def on_startup(bot: Bot) -> None:
    await create_db()
    await bot.set_webhook(
        f"{WEBHOOK_ADDRESS}{WEBHOOK_PATH}",
        secret_token=WEBHOOK_SECRET_TOKEN,
    )

async def delete_updates(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)

def main() -> None:
    loop = asyncio.new_event_loop()

    dp = Dispatcher()

    setup_aiogram(dp)

    dp.startup.register(on_startup)

    loop.run_until_complete(delete_updates(bot))

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET_TOKEN,
    )

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEBHOOK_LISTENING_HOST, port=WEBHOOK_LISTENING_PORT, loop=loop)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()