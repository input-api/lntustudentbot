from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class EventActions(Enum):
    my_events = "my_events"
    add_event = "add_event"

class EventCbData(CallbackData, prefix="actions_events"):
    action: EventActions


def actions_events_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Мої події", callback_data=EventCbData(action=EventActions.my_events).pack())
    builder.button(text="➕ Додати подію", callback_data=EventCbData(action=EventActions.add_event).pack())
    builder.button(text="🔙 Адмін-меню", callback_data="back_main_admin")
    builder.adjust(1)

    return builder.as_markup()

