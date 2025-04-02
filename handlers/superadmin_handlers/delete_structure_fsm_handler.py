from aiogram import F, Router
from aiogram.types import CallbackQuery

from kbds.superadmin.structure_actions_kbd import StructureOptCbData, StructureOptActions
from kbds.superadmin.main_kbd import back_main_superadmin

delete_structure_router = Router()

@delete_structure_router.callback_query(StructureOptCbData.filter(F.action == StructureOptActions.delete_structure))
async def delete_structure(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Видалити структуру",
        reply_markup=back_main_superadmin()
    )