from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def approve(action: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="✅ Так", callback_data=f"{action}_yes")
    builder.button(text="❌ Ні", callback_data=f"{action}_no")

    builder.adjust(2)

    return builder.as_markup()