from aiogram import F, Router
from aiogram.types import CallbackQuery

from handlers.admin_handlers.answer_for_question_handler import admin_answer_router
from kbds.admin.main_kbd import AdminCbData, AdminActions, back_to_main_admin
from kbds.admin.event_kbd import actions_events_keyboard
from kbds.admin.hostels_actions_kbd import hostels_actions_keyboard

main_admin_router = Router()
main_admin_router.include_router(admin_answer_router)

@main_admin_router.callback_query(AdminCbData.filter(F.action == AdminActions.edit_profile))
async def show_student_government_menu(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Редагувати свій профіль:",
        reply_markup=back_to_main_admin()
    )

@main_admin_router.callback_query(AdminCbData.filter(F.action == AdminActions.event))
async def show_events(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Дії з подіями:",
        reply_markup=actions_events_keyboard()
    )

@main_admin_router.callback_query(AdminCbData.filter(F.action == AdminActions.idea_from_stud))
async def students_propose_idea(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Вам пропонують ідею.",
        reply_markup=back_to_main_admin()
    )

@main_admin_router.callback_query(AdminCbData.filter(F.action == AdminActions.show_talents))
async def join_student(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Студенти хочуть проявити себе.",
        reply_markup=back_to_main_admin()
    )

@main_admin_router.callback_query(AdminCbData.filter(F.action == AdminActions.hostels_actions))
async def show_hostels_options(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Оберіть що цікавить:",
        reply_markup=hostels_actions_keyboard()
    )
