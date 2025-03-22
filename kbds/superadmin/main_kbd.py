from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class SuperAdminActions(Enum):
    admin = "admin"
    structure = "structure"

class SuperAdminCbData(CallbackData, prefix="superadmin"):
    action: SuperAdminActions

def super_admin_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Дії з адміном", callback_data=SuperAdminCbData(action=SuperAdminActions.admin).pack())
    builder.button(text="Дії з структурою", callback_data=SuperAdminCbData(action=SuperAdminActions.structure).pack())

    builder.adjust(1)

    return builder.as_markup()

def back_main_superadmin() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🔙 Sudo-меню", callback_data="back_main_superadmin")

    return builder.as_markup()