from aiogram import F, Router
from aiogram.types import CallbackQuery

from kbds.superadmin.structure_actions_kbd import StructureOptCbData, StructureOptActions
from kbds.superadmin.main_kbd import back_main_superadmin

edit_structure_router = Router()

@edit_structure_router.callback_query(StructureOptCbData.filter(F.action == StructureOptActions.edit_structure))
async def edit_structure(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Редагувати структуру",
        reply_markup=back_main_superadmin()
    )