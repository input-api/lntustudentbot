from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class HostelActions(Enum):
    problems = "problems"
    propose = "propose"


class HostelCbData(CallbackData, prefix="hostels_actions"):
    action: HostelActions


def hostels_actions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🔧 Проблеми", callback_data=HostelCbData(action=HostelActions.problems).pack())
    builder.button(text="💡 Пропозиції", callback_data=HostelCbData(action=HostelActions.propose).pack())
    builder.button(text="🔙 Адмін-меню", callback_data="back_main_admin")

    builder.adjust(2, 1)

    return builder.as_markup()

