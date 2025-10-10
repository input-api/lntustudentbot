from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

class MainActions(Enum):
    student_gov = "student_gov"
    events = "events"
    question = "question"
    propose_idea = "propose_idea"
    join_us = "join_us"
    hostels = "hostels"
    talents = "talents"
    # volunteer_hub = "volunteer_hub"
    login_as_admin = "login_as_admin"

class MainCbData(CallbackData, prefix="main"):
    action: MainActions

def main_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="📋 Студентське самоврядування", callback_data=MainCbData(action=MainActions.student_gov).pack())
    builder.button(text="📅 Заплановані заходи", callback_data=MainCbData(action=MainActions.events).pack())
    builder.button(text="📞 Зв'язок із студрадою", callback_data=MainCbData(action=MainActions.question).pack())
    builder.button(text="💡 Запропонувати ідею", callback_data=MainCbData(action=MainActions.propose_idea).pack())
    builder.button(text="🤝 Хочу вступити до студради", callback_data=MainCbData(action=MainActions.join_us).pack())
    # builder.button(text="🏠 Гуртожитки ЛНТУ", callback_data=MainCbData(action=MainActions.hostels).pack())
    builder.button(text="🌟 ЛНТУ має таланти", callback_data=MainCbData(action=MainActions.talents).pack())
    # builder.button(text="🤗 Волонтер-хаб", callback_data=MainCbData(action=MainActions.volunteer_hub).pack())

    builder.adjust(1)

    return builder.as_markup()

def back_to_main() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Головне меню", callback_data="back")

    return builder.as_markup()
