from aiogram import F, Router
from aiogram.types import CallbackQuery

from kbds.admin.main_kbd import back_to_main_admin
from kbds.admin.hostels_actions_kbd import HostelCbData, HostelActions

hostels_actions_router = Router()

@hostels_actions_router.callback_query(HostelCbData.filter(F.action == HostelActions.problems))
async def settle_in_hostel(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Проблеми вашого гуртожитку:",
        reply_markup=back_to_main_admin()
    )

@hostels_actions_router.callback_query(HostelCbData.filter(F.action == HostelActions.propose))
async def settle_in_hostel(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Пропозиції щодо проживання в гуртожитку:",
        reply_markup=back_to_main_admin()
    )
