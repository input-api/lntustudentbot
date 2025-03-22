from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class EventActions(Enum):
    add_event = "add_event"
    edit_event = "edit_event"
    delete_event = "delete_event"


class EventCbData(CallbackData, prefix="actions_events"):
    action: EventActions


def actions_events_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="➕", callback_data=EventCbData(action=EventActions.add_event).pack())
    builder.button(text="✏️", callback_data=EventCbData(action=EventActions.edit_event).pack())
    builder.button(text="🗑️", callback_data=EventCbData(action=EventActions.delete_event).pack())
    builder.button(text="🔙 Адмін-меню", callback_data="back_main_admin")
    builder.adjust(3, 1)

    return builder.as_markup()

