from aiogram import F, Router
from aiogram.types import CallbackQuery

from kbds.user.hostels_kbds import HostelsCbData, HostelsActions
from kbds.user.main_kbd import back_to_main

hostels_router = Router()

@hostels_router.callback_query(HostelsCbData.filter(F.action == HostelsActions.hostel_1), HostelsCbData.filter(F.option != ""))
async def options_hostel_1(callback_query: CallbackQuery):
    state, hostel, option = callback_query.data.split(":")
    if state == "hostels":
        await callback_query.message.edit_text(
            text=f"Ви хочете {option} в {hostel}",
            reply_markup=back_to_main()
        )

@hostels_router.callback_query(HostelsCbData.filter(F.action == HostelsActions.hostel_2), HostelsCbData.filter(F.option != ""))
async def options_hostel_1(callback_query: CallbackQuery):
    state, hostel, option = callback_query.data.split(":")
    if state == "hostels":
        await callback_query.message.edit_text(
            text=f"Ви хочете {option} в {hostel}",
            reply_markup=back_to_main()
        )

@hostels_router.callback_query(HostelsCbData.filter(F.action == HostelsActions.hostel_3), HostelsCbData.filter(F.option != ""))
async def options_hostel_1(callback_query: CallbackQuery):
    state, hostel, option = callback_query.data.split(":")
    if state == "hostels":
        await callback_query.message.edit_text(
            text=f"Ви хочете {option} в {hostel}",
            reply_markup=back_to_main()
        )