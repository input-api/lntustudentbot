from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class AdminActions(Enum):
    edit_profile = "edit_profile"
    event = "event"
    questions = "questions"
    idea_from_stud = "idea_from_stud"
    show_talents = "show_talents"
    hostels_actions = "hostels_actions"

class AdminCbData(CallbackData, prefix="admin"):
    action: AdminActions

def admin_keyboard(hostels_admin) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="✏️ Редагувати профіль", callback_data=AdminCbData(action=AdminActions.edit_profile).pack())
    builder.button(text="📅 Події", callback_data=AdminCbData(action=AdminActions.event).pack())
    builder.button(text="❓ Питання від студентів", callback_data=AdminCbData(action=AdminActions.questions).pack())
    builder.button(text="💡 Ідеї студентів", callback_data=AdminCbData(action=AdminActions.idea_from_stud).pack())
    builder.button(text="🌟 Таланти студентів", callback_data=AdminCbData(action=AdminActions.show_talents).pack())
    # if hostels_admin:
    #     builder.button(text="🏠 Гуртожитки", callback_data=AdminCbData(action=AdminActions.hostels_actions).pack())

    builder.adjust(1)

    return builder.as_markup()

def back_to_main_admin() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🔙 Адмін-меню", callback_data="back_main_admin")

    return builder.as_markup()