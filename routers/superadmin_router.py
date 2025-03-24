from aiogram import Router, F, types
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from filters.main_filters import IsSuperAdmin
from handlers.superadmin_handlers.main_kbd_handler import superadmin_main_router
from kbds.superadmin.admin_actions_kbd import admin_opt_actions_keyboard
from kbds.superadmin.main_kbd import super_admin_keyboard, SuperAdminCbData, SuperAdminActions, back_main_superadmin
from kbds.superadmin.structure_actions_kbd import structure_opt_actions_keyboard

super_admin_router = Router()
super_admin_router.message.filter(IsSuperAdmin())

super_admin_router.include_routers(superadmin_main_router)

@super_admin_router.callback_query(SuperAdminCbData.filter(F.action == SuperAdminActions.admin))
async def admin_options_actions(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Що робимо?",
        reply_markup=admin_opt_actions_keyboard()
    )

@super_admin_router.callback_query(SuperAdminCbData.filter(F.action == SuperAdminActions.structure))
async def structure_options_actions(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Що робимо?",
        reply_markup=structure_opt_actions_keyboard()
    )

@super_admin_router.callback_query(F.data == "back_main_superadmin")
async def back_main_admin(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text="Ви суперадмін:",
        reply_markup=super_admin_keyboard(),
    )


@super_admin_router.message(StateFilter("*"), F.text.in_({"cancel", "відміна", "exit", "вийти"}))
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Дії відмінено!", reply_markup=back_main_superadmin())