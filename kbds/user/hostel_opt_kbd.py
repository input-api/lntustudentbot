from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class HostelsOptionActions(Enum):
    settle_in = "settle_in"
    problems = "problems"
    complaint = "complaint"


class HostelsOptionCbData(CallbackData, prefix="hostels"):
    action: HostelsOptionActions


def hostel_option_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="📄 Заява на поселення", callback_data=HostelsOptionCbData(action=HostelsOptionActions.settle_in).pack())
    builder.button(text="🔧 Проблеми, потреби", callback_data=HostelsOptionCbData(action=HostelsOptionActions.problems).pack())
    builder.button(text="✉️ Скарги, пропозиції", callback_data=HostelsOptionCbData(action=HostelsOptionActions.complaint).pack())
    builder.button(text="🏡 Головне меню", callback_data="back")

    builder.adjust(1)

    return builder.as_markup()