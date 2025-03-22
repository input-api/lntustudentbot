from aiogram import F, Router
from aiogram.types import CallbackQuery

from handlers.superadmin_handlers.add_admin_fsm_handler import add_admin_router
from handlers.superadmin_handlers.add_structure_fsm_handler import add_structure_router
from kbds.superadmin.admin_actions_kbd import AdminOptCbData, AdminOptActions
from kbds.superadmin.main_kbd import back_main_superadmin

superadmin_main_router = Router()
superadmin_main_router.include_routers(add_admin_router, add_structure_router)


@superadmin_main_router.callback_query(AdminOptCbData.filter(F.action == AdminOptActions.edit_admin))
async def edit_admin(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Редагувати адміна.",
        reply_markup=back_main_superadmin()
    )

@superadmin_main_router.callback_query(AdminOptCbData.filter(F.action == AdminOptActions.delete_admin))
async def delete_admin(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Видалити адміна.",
        reply_markup=back_main_superadmin()
    )

