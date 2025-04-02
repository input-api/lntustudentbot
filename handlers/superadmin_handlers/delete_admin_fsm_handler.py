from aiogram import F, Router
from aiogram.types import CallbackQuery

from kbds.superadmin.admin_actions_kbd import AdminOptCbData, AdminOptActions
from kbds.superadmin.main_kbd import back_main_superadmin

delete_admin_router = Router()

@delete_admin_router.callback_query(AdminOptCbData.filter(F.action == AdminOptActions.delete_admin))
async def delete_admin(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Редагувати адміна.",
        reply_markup=back_main_superadmin()
    )