from aiogram import F, Router
from aiogram.types import CallbackQuery

from handlers.user_handlers.propose_idea_fsm_handler import propose_idea_router
from kbds.user.faculty_kbd import faculty_keyboard
from kbds.user.hostel_opt_kbd import hostel_option_keyboard
from kbds.user.main_kbd import MainActions, MainCbData, back_to_main
from kbds.user.gov_kbd import gov_keyboard

main_menu_router = Router()
main_menu_router.include_router(propose_idea_router)

@main_menu_router.callback_query(MainCbData.filter(F.action == MainActions.student_gov))
async def show_student_government_menu(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Що з студентського свмоврядування вас цікавить?",
        reply_markup=gov_keyboard()
    )

@main_menu_router.callback_query(MainCbData.filter(F.action == MainActions.question))
async def students_questions(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="З ким ви хочете зв'язатись?",
        reply_markup=faculty_keyboard(previous_action="question", plus_general_gov_and_profcom=True)
    )

@main_menu_router.callback_query(MainCbData.filter(F.action == MainActions.propose_idea))
async def students_propose_idea(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Що хочете запропонувати?",
        reply_markup=faculty_keyboard(previous_action="propose_idea", plus_general_gov_and_profcom=True)
    )

@main_menu_router.callback_query(MainCbData.filter(F.action == MainActions.join_us))
async def join_student(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Куди ви хочете доєднатись?",
        reply_markup=gov_keyboard(remove=True)
    )

@main_menu_router.callback_query(MainCbData.filter(F.action == MainActions.hostels))
async def show_hostels_options(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Що про гуртожитки ви хочете дізнатись?",
        reply_markup=hostel_option_keyboard()
    )

@main_menu_router.callback_query(MainCbData.filter(F.action == MainActions.talents))
async def students_talents(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Як ви хочете себе проявити?",
        reply_markup=back_to_main()
    )

@main_menu_router.callback_query(MainCbData.filter(F.action == MainActions.volunteer_hub))
async def students_talents(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="text=Про волонтер-хаб, button=доєднатись",
        reply_markup=back_to_main()
    )

@main_menu_router.callback_query(MainCbData.filter(F.action == MainActions.volunteer_hub))
async def students_talents(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="text=Про волонтер-хаб, button=доєднатись",
        reply_markup=back_to_main()
    )