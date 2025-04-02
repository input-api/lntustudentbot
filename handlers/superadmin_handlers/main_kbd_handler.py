from aiogram import F, Router
from aiogram.types import CallbackQuery

from handlers.superadmin_handlers.add_admin_fsm_handler import add_admin_router
from handlers.superadmin_handlers.add_structure_fsm_handler import add_structure_router
from handlers.superadmin_handlers.delete_admin_fsm_handler import delete_admin_router
from handlers.superadmin_handlers.delete_structure_fsm_handler import delete_structure_router
from handlers.superadmin_handlers.edit_admin_fsm_handler import edit_admin_router
from handlers.superadmin_handlers.edit_structure_fsm_handler import edit_structure_router
from kbds.superadmin.main_kbd import super_admin_keyboard

superadmin_main_router = Router()
superadmin_main_router.include_routers(add_admin_router, add_structure_router, edit_structure_router, edit_admin_router, delete_structure_router, delete_admin_router)

@superadmin_main_router.callback_query(F.data == "back_main_superadmin")
async def back_main_admin(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Ви суперадмін:",
        reply_markup=super_admin_keyboard(),
    )