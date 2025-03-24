from aiogram import F, Router
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from db.orm_query import orm_get_admins_events, orm_get_admins_events
from kbds.admin.event_action_kbd import events_act_keyboard
from kbds.admin.main_kbd import back_to_main_admin
from kbds.admin.my_event_kbd import MyEventCbData, MyEventActions
from kbds.admin.my_event_kbd import my_events_keyboard

my_event_router = Router()

@my_event_router.callback_query(MyEventCbData.filter(F.action == MyEventActions.published))
async def published_events(callback_query: CallbackQuery, session: AsyncSession()):
    admin_id = callback_query.from_user.id
    data = await orm_get_admins_events(session, admin_id, True)

    if not data:
        await callback_query.message.edit_text(
            text="Ви ще не створювали події або вони вже минули.",
            reply_markup=back_to_main_admin()
        )

    else:
        text = "\n".join([f"🆔:{event.id} - {event.title}" for event in data])
        await callback_query.message.edit_text(
            text=f"Доступні події:\n\n{text}",
            reply_markup=events_act_keyboard(True)
        )

@my_event_router.callback_query(MyEventCbData.filter(F.action == MyEventActions.unpublished))
async def published_events(callback_query: CallbackQuery, session: AsyncSession()):
    admin_id = callback_query.from_user.id
    data = await orm_get_admins_events(session, admin_id, False)

    if not data:
        await callback_query.message.edit_text(
            text="Ви ще не створювали події або вони вже минули.",
            reply_markup=back_to_main_admin()
        )

    else:
        text = "\n".join([f"🆔:{event.id} - {event.title}" for event in data])
        await callback_query.message.edit_text(
            text=f"Доступні події:\n\n{text}",
            reply_markup=events_act_keyboard(False)
        )
