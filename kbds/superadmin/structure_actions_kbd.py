from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class  StructureOptActions(Enum):
    add_structure = "add_structure"
    edit_structure = "edit_structure"
    delete_structure = "delete_structure"

class StructureOptCbData(CallbackData, prefix="structure_options"):
    action: StructureOptActions

def structure_opt_actions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="➕ Додати структуру", callback_data=StructureOptCbData(action=StructureOptActions.add_structure).pack())
    builder.button(text="✏️ Редагувати структуру", callback_data=StructureOptCbData(action=StructureOptActions.edit_structure).pack())
    builder.button(text="🗑️ Видалити структуру", callback_data=StructureOptCbData(action=StructureOptActions.delete_structure).pack())
    builder.button(text="🔙 Sudo-меню", callback_data="back_main_superadmin")

    builder.adjust(1)

    return builder.as_markup()