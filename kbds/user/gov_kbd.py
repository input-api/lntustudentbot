from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class GovActions(Enum):
    profcom = "profcom"
    general_gov = "general_gov"
    faculties_gov = "faculties_gov"
    hostels = "hostels"

class GovCbData(CallbackData, prefix="gov"):
    action: GovActions
    prev: str


def gov_keyboard(remove = False, param="") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="👥 Профком", callback_data=GovCbData(action=GovActions.profcom, prev=param).pack())

    if not remove:
        builder.button(text="🏛️ Загальна студрада", callback_data=GovCbData(action=GovActions.general_gov, prev=param).pack())
        builder.button(text="🏠 Гуртожитки", callback_data=GovCbData(action=GovActions.hostels, prev=param).pack())

    builder.button(text="📚 Студради факультетів", callback_data=GovCbData(action=GovActions.faculties_gov, prev=param).pack())
    builder.button(text="🏡 Головне меню", callback_data="back")

    builder.adjust(1)

    return builder.as_markup()
