import locale

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from bot_setup import get_bot
from db.orm_query import orm_get_published_events, orm_get_poster_by_event_id
from kbds.user.main_kbd import MainCbData, MainActions, main_keyboard

view_event = Router()

class EventState(StatesGroup):
    messages = State()

@view_event.callback_query(MainCbData.filter(F.action == MainActions.events))
async def show_events(callback_query: CallbackQuery, session: AsyncSession, state: FSMContext):
    events = await orm_get_published_events(session)
    locale.setlocale(locale.LC_TIME, "uk_UA.UTF-8")

    sm_id = callback_query.message.message_id
    messages_to_delete = [sm_id]

    builder = InlineKeyboardBuilder()
    builder.button(text="🏡 Головне меню", callback_data="back_to_main_from_events")
    to_main = builder.as_markup()

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

        markup = to_main if index == len(events) - 1 else None

        message = await callback_query.message.answer_photo(
            photo=photo,
            caption=caption_text,
            parse_mode="HTML",
            reply_markup=markup
        )

        messages_to_delete.append(message.message_id)
    await state.update_data(messages_to_delete=messages_to_delete)

@view_event.callback_query(F.data == "back_to_main_from_events")
async def back_to_main_from_events(callback_query: CallbackQuery, state: FSMContext):
    bot = get_bot()
    data = await state.get_data()
    messages_to_delete = data.get("messages_to_delete", [])
    for msg_id in messages_to_delete:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=msg_id)

    await callback_query.message.answer(
        text="Головне меню:",
        reply_markup=main_keyboard(),
    )