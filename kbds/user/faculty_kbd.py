from enum import Enum
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class FacultyActions(Enum):
    fkit = "fkit"
    fmmt = "fmmt"
    fbp = "fbp"
    ftsost = "ftsost"
    ftmi = "ftmi"
    fate = "fate"
    fabd = "fabd"
    general_gov = "general_gov"
    profcom = "profcom"


class FacultyCbData(CallbackData, prefix="faculty"):
    action: FacultyActions
    previous_action: str


def faculty_keyboard(previous_action, plus_general_gov_and_profcom = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="ФКІТ", callback_data=FacultyCbData(action=FacultyActions.fkit, previous_action=previous_action).pack())
    builder.button(text="ФММТ", callback_data=FacultyCbData(action=FacultyActions.fmmt, previous_action=previous_action).pack())
    builder.button(text="ФБП", callback_data=FacultyCbData(action=FacultyActions.fbp, previous_action=previous_action).pack())

    builder.button(text="ФЦОСТ", callback_data=FacultyCbData(action=FacultyActions.ftsost, previous_action=previous_action).pack())
    builder.button(text="ФТМІ", callback_data=FacultyCbData(action=FacultyActions.ftmi, previous_action=previous_action).pack())
    builder.button(text="ФАТЕ", callback_data=FacultyCbData(action=FacultyActions.fate, previous_action=previous_action).pack())
    builder.button(text="ФАБД", callback_data=FacultyCbData(action=FacultyActions.fabd, previous_action=previous_action).pack())

    if plus_general_gov_and_profcom:
        builder.button(text="Загальна студрада", callback_data=FacultyCbData(action=FacultyActions.general_gov, previous_action=previous_action).pack())
        builder.button(text="Профком", callback_data=FacultyCbData(action=FacultyActions.profcom, previous_action=previous_action).pack())

    builder.button(text="🏡 Головне меню", callback_data="back")

    builder.adjust(4,3,1)

    if plus_general_gov_and_profcom:
        builder.adjust(4,3,2,1)

    return builder.as_markup()
