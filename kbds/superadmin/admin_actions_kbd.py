from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class AdminOptActions(Enum):
    add_admin = "add_admin"
    edit_admin = "edit_admin"
    delete_admin = "delete_admin"

class AdminOptCbData(CallbackData, prefix="admin_options"):
    action: AdminOptActions

def admin_opt_actions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="➕ Додати адміна", callback_data=AdminOptCbData(action=AdminOptActions.add_admin).pack())
    builder.button(text="✏️ Редагувати адміна", callback_data=AdminOptCbData(action=AdminOptActions.edit_admin).pack())
    builder.button(text="🗑️ Видалити адміна", callback_data=AdminOptCbData(action=AdminOptActions.delete_admin).pack())
    builder.button(text="🔙 Sudo-меню", callback_data="back_main_superadmin")

    builder.adjust(1)

    return builder.as_markup()