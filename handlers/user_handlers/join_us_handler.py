from aiogram import F, Router
from aiogram.types import CallbackQuery

from kbds.user.faculty_kbd import faculty_keyboard
from kbds.user.gov_kbd import GovCbData, GovActions
from kbds.user.main_kbd import back_to_main

join_us_router = Router()

@join_us_router.callback_query(GovCbData.filter(F.action == GovActions.faculties_gov), GovCbData.filter(F.prev == "join_us"))
async def show_faculties_government_menu(callback_query: CallbackQuery):
    action = callback_query.data.split(":")[2]
    await callback_query.message.edit_text(
        text="Оберіть студраду:",
        reply_markup=faculty_keyboard(previous_action=action)
    )