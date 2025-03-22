from aiogram import F, Router
from aiogram.types import CallbackQuery

from kbds.user.hostel_opt_kbd import HostelsOptionCbData, HostelsOptionActions
from kbds.user.hostels_kbds import hostels_keyboard

hostel_option_router = Router()

@hostel_option_router.callback_query(HostelsOptionCbData.filter(F.action == HostelsOptionActions.settle_in))
async def settle_in_hostel(callback_query: CallbackQuery):
    state, option = callback_query.data.split(":")
    if state == "hostels":
        await callback_query.message.edit_text(
            text="Оберіть гуртожиток:",
            reply_markup=hostels_keyboard(option=option)
        )

@hostel_option_router.callback_query(HostelsOptionCbData.filter(F.action == HostelsOptionActions.problems))
async def settle_in_hostel(callback_query: CallbackQuery):
    state, option = callback_query.data.split(":")
    if state == "hostels":
        await callback_query.message.edit_text(
            text="Оберіть гуртожиток:",
            reply_markup=hostels_keyboard(option=option)
        )

@hostel_option_router.callback_query(HostelsOptionCbData.filter(F.action == HostelsOptionActions.complaint))
async def settle_in_hostel(callback_query: CallbackQuery):
    state, option = callback_query.data.split(":")
    if state == "hostels":
        await callback_query.message.edit_text(
            text="Оберіть гуртожиток:",
            reply_markup=hostels_keyboard(option=option)
        )