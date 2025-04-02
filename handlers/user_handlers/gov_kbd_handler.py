from aiogram import F, Router
from aiogram.types import CallbackQuery

from kbds.user.faculty_kbd import faculty_keyboard
from kbds.user.gov_kbd import GovCbData, GovActions
from kbds.user.hostels_kbds import hostels_keyboard
from kbds.user.main_kbd import back_to_main

government_router = Router()

@government_router.callback_query(GovCbData.filter(F.action == GovActions.profcom))
async def show_profcom_menu(callback_query: CallbackQuery):
    action = callback_query.data.split(":")[1]
    await callback_query.message.edit_text(
        text="Ви обрали профком",
        reply_markup=back_to_main()
    )

@government_router.callback_query(GovCbData.filter(F.action == GovActions.faculties_gov), GovCbData.filter(F.prev == "student_gov"))
async def show_faculties_government_menu(callback_query: CallbackQuery):
    action = callback_query.data.split(":")[1]
    await callback_query.message.edit_text(
        text="Оберіть студраду:",
        reply_markup=faculty_keyboard(previous_action=action)
    )

@government_router.callback_query(GovCbData.filter(F.action == GovActions.hostels))
async def show_hostels_government_menu(callback_query: CallbackQuery):
    action = callback_query.data.split(":")[0]
    await callback_query.message.edit_text(
        text="Оберіть гуртожиток:",
        reply_markup=hostels_keyboard(previous_action=action, option="")
    )