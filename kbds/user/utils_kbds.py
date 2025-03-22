from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def yes_or_no_kbd() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="✅ Так", callback_data="event_notifications_yes")
    builder.button(text="❌ Ні", callback_data="event_notifications_no")

    builder.adjust(2)

    return builder.as_markup()