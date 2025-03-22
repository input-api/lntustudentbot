from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def approve() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="✅ Так", callback_data=f"yes")
    builder.button(text="❌ Ні", callback_data=f"no")

    builder.adjust(2)

    return builder.as_markup()