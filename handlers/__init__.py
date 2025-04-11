from aiogram import Dispatcher, F
from aiogram.filters import CommandStart, Command

from filters.main_filters import IsAdmin
from handlers.base import Handler
from handlers.start import process, start_with_admin, start


def prepare_router(dp: Dispatcher):
    start_handlers = [
        Handler(process, [Command("updsudo")]),
        Handler(start_with_admin, [Command("start"), IsAdmin()]),
        Handler(start, [Command("start"), ~IsAdmin()]),
    ]
    for handler in start_handlers:
        dp.message.register(handler.handler, *handler.filters)
