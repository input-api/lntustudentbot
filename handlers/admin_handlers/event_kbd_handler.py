from aiogram import F, Router
from aiogram.types import CallbackQuery

from kbds.admin.main_kbd import back_to_main_admin
from kbds.admin.event_kbd import EventCbData, EventActions

event_action_router = Router()

@event_action_router.callback_query(EventCbData.filter(F.action == EventActions.add_event))
async def admin_add_event(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Додати подію.",
        reply_markup=back_to_main_admin()
    )

@event_action_router.callback_query(EventCbData.filter(F.action == EventActions.edit_event))
async def admin_edit_event(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Редагувати подію.",
        reply_markup=back_to_main_admin()
    )

@event_action_router.callback_query(EventCbData.filter(F.action == EventActions.delete_event))
async def admin_delete_event(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Видалити подію.",
        reply_markup=back_to_main_admin()
    )
