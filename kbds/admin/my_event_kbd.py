from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MyEventActions(Enum):
    published = "published"
    unpublished = "unpublished"

class MyEventCbData(CallbackData, prefix="my_events"):
    action: MyEventActions


def my_events_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Опубліковані", callback_data=MyEventCbData(action=MyEventActions.published).pack())
    builder.button(text="Не опубліковані", callback_data=MyEventCbData(action=MyEventActions.unpublished).pack())
    builder.button(text="🔙 Адмін-меню", callback_data="back_main_admin")
    builder.adjust(1)

    return builder.as_markup()

