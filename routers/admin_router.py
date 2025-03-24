from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from filters.main_filters import IsAdmin
from handlers.admin_handlers.main_kbd_handler import main_admin_router
from handlers.admin_handlers.event_kbd_handler import event_action_router
from handlers.admin_handlers.hostels_actions_kbd_handler import hostels_actions_router
from kbds.admin.main_kbd import admin_keyboard, back_to_main_admin

admin_router = Router()
admin_router.message.filter(IsAdmin())

admin_router.include_routers(main_admin_router, hostels_actions_router, event_action_router)

@admin_router.callback_query(F.data == "back_main_admin")
async def back_main_admin(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text="Адмін-меню:",
        reply_markup=admin_keyboard(True),
    )

@admin_router.message(StateFilter("*"), F.text.in_({"cancel", "відміна", "exit", "вийти"}))
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Дії відмінено!", reply_markup=back_to_main_admin())