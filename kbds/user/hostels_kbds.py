from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class HostelsActions(Enum):
    hostel_1 = "h1"
    hostel_2 = "h2"
    hostel_3 = "h3"


class HostelsCbData(CallbackData, prefix="hostels"):
    action: HostelsActions
    previous_action: str
    option: str


def hostels_keyboard(previous_action, option) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Гуртожиток №1", callback_data=HostelsCbData(action=HostelsActions.hostel_1, previous_action = previous_action, option=option).pack())
    builder.button(text="Гуртожиток №2", callback_data=HostelsCbData(action=HostelsActions.hostel_2, previous_action = previous_action, option=option).pack())
    builder.button(text="Гуртожиток №3", callback_data=HostelsCbData(action=HostelsActions.hostel_3, previous_action = previous_action, option=option).pack())
    builder.button(text="🏡 Головне меню", callback_data="back")

    builder.adjust(1)

    return builder.as_markup()