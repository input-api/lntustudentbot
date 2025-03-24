from aiogram import F, Router
from aiogram.types import CallbackQuery

from handlers.admin_handlers.add_event_handler import add_event_router
from handlers.admin_handlers.event_act_kbd_handler import event_act_router
from handlers.admin_handlers.my_event_handler import my_event_router
from kbds.admin.event_kbd import EventCbData, EventActions
from kbds.admin.my_event_kbd import my_events_keyboard

event_action_router = Router()
event_action_router.include_routers(add_event_router, my_event_router, event_act_router)

@event_action_router.callback_query(EventCbData.filter(F.action == EventActions.my_events))
async def admin_events(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Які події хочете побачити?",
        reply_markup=my_events_keyboard()
    )
