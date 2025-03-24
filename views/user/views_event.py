import locale

from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from db.orm_query import orm_get_published_events, orm_get_poster_by_event_id
from kbds.user.main_kbd import MainCbData, MainActions, back_to_main

view_event = Router()

@view_event.callback_query(MainCbData.filter(F.action == MainActions.events))
async def show_events(callback_query: CallbackQuery, session: AsyncSession):
    events = await orm_get_published_events(session)
    locale.setlocale(locale.LC_TIME, "uk_UA.UTF-8")
    for index, event in enumerate(events):
        date_part = event.date_time_start.strftime("%d %B")
        time_part = event.date_time_start.strftime("%H:%M")
        event_id = event.id
        photo = await orm_get_poster_by_event_id(session, event_id)

        caption_text = (
            f"<b>{event.title}</b>\n\n"
            f"📅Дата: {date_part}\n"
            f"🕘Час: {time_part}\n"
            f"📍Локація: {event.location}\n"
            f"🧑‍💼Організатор: {event.organizer}\n\n"
            f"{event.description}\n\n"
        )

        await callback_query.message.answer_photo(
            photo=photo,
            caption=caption_text,
            parse_mode="HTML"
        )
