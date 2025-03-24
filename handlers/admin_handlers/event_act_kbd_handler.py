from datetime import datetime
import re

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from bot_setup import get_bot
from db.orm_query import orm_get_admins_events_id_list, orm_get_date_time_start_event, orm_update_event, \
    orm_update_event_poster, orm_delete_event_by_id, orm_get_all_user_with_event_notification, \
    orm_get_scheduled_event_by_id, orm_get_poster_by_event_id
from fsm.admin.fsm_delete_event import DeleteEvent
from fsm.admin.fsm_edit_event import EditEvent
from fsm.admin.fsm_publish_event import PublishEvent
from fsm.admin.fsm_unpublish_event import UnpublishEvent
from handlers.admin_handlers.utils import approve
from kbds.admin.event_action_kbd import EventActCbData, EventActActions
from kbds.admin.main_kbd import admin_keyboard, back_to_main_admin

event_act_router = Router()

@event_act_router.callback_query(EventActCbData.filter(F.action == EventActActions.edit_event))
async def edit_event(callback_query: CallbackQuery, state: FSMContext):
    prev_text = callback_query.message.text
    await state.update_data(sm_id=callback_query.message.message_id - 1)
    await state.set_state(EditEvent.get_id_event)
    await callback_query.message.edit_text(
        text=f"{prev_text}\n\n"
             "Введіть id події, яку хочете редагувати:",
    )

@event_act_router.message(EditEvent.get_id_event, F.text)
async def get_id_event_for_edit(message: Message, session: AsyncSession, state: FSMContext):
    admin_id = message.from_user.id
    event_list_id = await orm_get_admins_events_id_list(session, admin_id, False, False)
    event_id = int(message.text)

    if event_id in event_list_id:
        await state.update_data(event_id = event_id)
        await state.set_state(EditEvent.get_param_for_change)
        await message.answer(
            text="Введіть параметр для редагування:\n"
                 "заголовок, опис, дата, час, місце, організатор, афіша",
        )
    else:
        await state.set_state(EditEvent.get_id_event)
        await message.answer(
            text="Не коректний id або події не існує. Спробуйте знову!",
        )

@event_act_router.message(EditEvent.get_param_for_change, F.text)
async def get_param_event_for_edit(message: Message, state: FSMContext):
    param = ""
    param_text = message.text
    match param_text.lower():
        case "заголовок":
            param = "title"
        case "опис":
            param = "description"
        case "дата":
            param = "date_start"
        case "час":
            param = "time_start"
        case "місце":
            param = "location"
        case "організатор":
            param = "organizer"
        case "афіша":
            await state.set_state(EditEvent.set_photo)
            await message.answer(
                text="Надішліть нову афішу:"
            )
            return
        case _:
            await state.set_state(EditEvent.get_param_for_change)
            await message.answer(
                text="Не коректний параметр. Спробуйте знову."
            )
            return

    await state.update_data(param=param)
    await state.set_state(EditEvent.update_event)
    await message.answer(
        "Введіть нове значення:"
    )

@event_act_router.message(EditEvent.set_photo, F.photo)
async def set_new_event_photo(message: Message, session: AsyncSession, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    data = await state.get_data()
    event_id = data["event_id"]

    user_id = message.from_user.id
    em_id = message.message_id+1
    bot = get_bot()
    on_delete = list(range(data["sm_id"], em_id))
    await bot.delete_messages(chat_id=user_id, message_ids=on_delete)

    await state.clear()
    await orm_update_event_poster(session, event_id, file_id)
    await message.answer(
        text="Афішу оновлено",
        reply_markup=back_to_main_admin()
    )

@event_act_router.message(EditEvent.set_photo)
async def set_new_event_photo_invalid(message: Message, state: FSMContext):
    await message.answer(
        text="Надішліть фото афіші.",
    )

@event_act_router.message(EditEvent.update_event, F.text)
async def get_update_event(message: Message, session: AsyncSession, state: FSMContext):
    value = message.text
    data = await state.update_data(updated_data = value)
    param = data["param"]
    event_id = data["event_id"]
    error = False

    text = "Подію оновлено"

    match param:
        case "title":
            if not isinstance(value, str) or not value:
                error = True
                text = "Некоректна назва. Перегляньте та спробуйте ще раз."
        case "description":
            if not isinstance(value, str) or not value:
                error = True
                text = "Некоректний опис. Перегляньте та спробуйте ще раз."
        case "date_start":
            if not re.match(r"(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0,1,2])\.(19|20)\d{2}", value):
                error = True
                text = "Впишіть дату за форматом DD.MM.YYYY, або перегляньте можливо ви ввели неіснуючу дату."
        case "time_start":
            if not re.match(r"^(?:([01][0-9]|2[0-3]):([0-5][0-9]))$", value):
                error = True
                text = "Впишіть час за форматом HH:MM, або перегляньте можливо ви ввели неіснуючий час."
        case "location":
            if not isinstance(value, str) or not value:
                error = True
                text = "Впишіть коректно локацію."
        case "organizer":
            if not isinstance(value, str) or not value:
                error = True
                text = "Впишіть коректно організатора."

    prev_date_time = await orm_get_date_time_start_event(session=session, event_id=event_id)

    if error:
        await state.set_state(EditEvent.update_event)
        await message.answer(text=text)
        return
    elif param == "date_start":
        time_part = prev_date_time.strftime("%H:%M")
        datetime_str = f"{value} {time_part}"
        new_datetime = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")
        await orm_update_event(session, event_id=event_id, date_time_start = new_datetime)
    elif param == "time_start":
        date_part = prev_date_time.strftime("%d.%m.%Y")
        datetime_str = f"{date_part} {value}"
        new_datetime = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")
        await orm_update_event(session, event_id=event_id, date_time_start = new_datetime)
    else:
        await orm_update_event(session, event_id=event_id, **{param: value})

    user_id = message.from_user.id
    em_id = message.message_id+1
    bot = get_bot()
    on_delete = list(range(data["sm_id"], em_id))
    await bot.delete_messages(chat_id=user_id, message_ids=on_delete)

    await message.answer(
        text=text,
        reply_markup=back_to_main_admin()
    )


@event_act_router.callback_query(EventActCbData.filter(F.action == EventActActions.delete_event))
async def delete_event(callback_query: CallbackQuery, state: FSMContext):
    prev_text = callback_query.message.text
    await state.update_data(sm_id=callback_query.message.message_id-1)
    await state.set_state(DeleteEvent.get_id_event)
    await callback_query.message.edit_text(
        text=f"{prev_text}\n\n"
        "Введіть id події, яку хочете видалити:",
    )

@event_act_router.message(DeleteEvent.get_id_event, F.text)
async def get_id_event_for_delete(message: Message, session: AsyncSession, state: FSMContext):
    admin_id = message.from_user.id
    event_list_id = await orm_get_admins_events_id_list(session, admin_id, False, False)
    event_id = int(message.text)

    if event_id in event_list_id:
        await state.update_data(event_id = event_id)
        await state.set_state(DeleteEvent.approve_delete)
        await message.answer(
            text="Підтвердіть видалення події:",
            reply_markup=approve("delete_event")
        )
    else:
        await state.set_state(DeleteEvent.get_id_event)
        await message.answer(
            text="Не коректний id або події не існує. Спробуйте знову!",
        )

@event_act_router.callback_query(DeleteEvent.approve_delete, F.data == "delete_event_yes")
async def delete_event(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    user_id = callback_query.from_user.id
    data = await state.update_data(em_id = callback_query.message.message_id+1)

    event_id = int(data["event_id"])

    bot = get_bot()
    await orm_delete_event_by_id(session, event_id)

    on_delete = list(range(data["sm_id"], data["em_id"]))
    await bot.delete_messages(chat_id=user_id, message_ids=on_delete)

    await state.clear()
    await callback_query.message.answer(
        "Подію видалено.",
        reply_markup=back_to_main_admin()
    )

@event_act_router.callback_query(DeleteEvent.approve_delete, F.data == "delete_event_no")
async def cancel_delete_event(callback_query: CallbackQuery, state: FSMContext):
    data = await state.update_data(em_id = callback_query.message.message_id+1)
    chat_id = callback_query.from_user.id
    bot = get_bot()
    on_delete = list(range(data["sm_id"],data["em_id"]))
    await bot.delete_messages(chat_id=chat_id,message_ids=on_delete)
    await state.clear()
    await callback_query.message.answer(
        text="Ви відмінили видалення події.",
        reply_markup=back_to_main_admin()
    )


@event_act_router.callback_query(EventActCbData.filter(F.action == EventActActions.unpublish_event))
async def unpublish_event(callback_query: CallbackQuery, state: FSMContext):
    prev_text = callback_query.message.text
    await state.update_data(sm_id=callback_query.message.message_id - 1)
    await state.set_state(UnpublishEvent.get_id_event)
    await callback_query.message.edit_text(
        text=f"{prev_text}\n\n"
             "Введіть id події, яку хочете зняти з публікації:",
    )

@event_act_router.message(UnpublishEvent.get_id_event, F.text)
async def get_id_event_for_unpublish(message: Message, session: AsyncSession, state: FSMContext):
    admin_id = message.from_user.id
    event_list_id = await orm_get_admins_events_id_list(session, admin_id, True, True)
    event_id = int(message.text)

    if event_id in event_list_id:
        await state.update_data(event_id = event_id)
        await state.set_state(UnpublishEvent.approve)
        await message.answer(
            text="Підтвердіть зняття з публікації:",
            reply_markup=approve("unpublish_event")
        )
    else:
        await state.set_state(UnpublishEvent.get_id_event)
        await message.answer(
            text="Не коректний id або події не існує. Спробуйте знову!",
        )

@event_act_router.callback_query(UnpublishEvent.approve, F.data == "unpublish_event_yes")
async def unpublish_event(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    user_id = callback_query.from_user.id
    data = await state.update_data(em_id = callback_query.message.message_id+1)

    event_id = int(data["event_id"])

    bot = get_bot()
    await orm_update_event(session, event_id, published = False)

    on_delete = list(range(data["sm_id"], data["em_id"]))
    await bot.delete_messages(chat_id=user_id, message_ids=on_delete)

    await state.clear()
    await callback_query.message.answer(
        "Подію знято з публікації.",
        reply_markup=back_to_main_admin()
    )

@event_act_router.callback_query(UnpublishEvent.approve, F.data == "unpublish_event_no")
async def cancel_unpublish_event(callback_query: CallbackQuery, state: FSMContext):
    data = await state.update_data(em_id = callback_query.message.message_id+1)
    chat_id = callback_query.from_user.id
    bot = get_bot()
    on_delete = list(range(data["sm_id"],data["em_id"]))
    await bot.delete_messages(chat_id=chat_id,message_ids=on_delete)
    await state.clear()
    await callback_query.message.answer(
        text="Ви відмінили зняття з публікації події.",
        reply_markup=back_to_main_admin()
    )

@event_act_router.callback_query(EventActCbData.filter(F.action == EventActActions.publish_event))
async def publish_event(callback_query: CallbackQuery, state: FSMContext):
    prev_text = callback_query.message.text
    await state.update_data(sm_id=callback_query.message.message_id - 1)
    await state.set_state(PublishEvent.get_id_event)
    await callback_query.message.edit_text(
        text=f"{prev_text}\n\n"
             "Введіть id події, яку хочете опублікувати:",
    )

@event_act_router.message(PublishEvent.get_id_event, F.text)
async def get_id_event_for_publish(message: Message, session: AsyncSession, state: FSMContext):
    admin_id = message.from_user.id
    event_list_id = await orm_get_admins_events_id_list(session, admin_id, True, False)
    event_id = int(message.text)

    if event_id in event_list_id:
        await state.update_data(event_id = event_id)
        await state.set_state(PublishEvent.approve)
        await message.answer(
            text="Підтвердіть публікацію:",
            reply_markup=approve("publish_event")
        )
    else:
        await state.set_state(PublishEvent.get_id_event)
        await message.answer(
            text="Не коректний id або події не існує. Спробуйте знову!",
        )

import asyncio

async def send_event_to_user(bot, user_id, photo, caption_text):
    try:
        await bot.send_photo(
            chat_id=user_id,
            photo=photo,
            caption=caption_text,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Помилка відправлення користувачу {user_id}: {e}")

@event_act_router.callback_query(PublishEvent.approve, F.data == "publish_event_yes")
async def publish_event(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    user_id = callback_query.from_user.id
    data = await state.update_data(em_id=callback_query.message.message_id + 1)

    event_id = int(data["event_id"])

    bot = get_bot()
    await orm_update_event(session, event_id, published=True)
    event = await orm_get_scheduled_event_by_id(session, event_id)
    date_part = event.date_time_start.strftime("%d.%m.%Y")
    time_part = event.date_time_start.strftime("%H:%M")

    caption_text = (
        f"<b>{event.title}</b>\n\n"
        f"📅Дата: {date_part}\n"
        f"🕘Час: {time_part}\n"
        f"📍Локація: {event.location}\n"
        f"🧑‍💼Організатор: {event.organizer}\n\n"
        f"{event.description}\n\n"
    )

    photo = await orm_get_poster_by_event_id(session, event_id)
    list_for_sent = await orm_get_all_user_with_event_notification(session)

    # Видалення попередніх повідомлень
    on_delete = list(range(data["sm_id"], data["em_id"]))
    await bot.delete_messages(chat_id=user_id, message_ids=on_delete)

    await state.clear()
    await callback_query.message.answer(
        "Подію опубліковано.",
        reply_markup=back_to_main_admin()
    )

    tasks = [send_event_to_user(bot, user, photo, caption_text) for user in list_for_sent]
    await asyncio.gather(*tasks)


@event_act_router.callback_query(PublishEvent.approve, F.data == "publish_event_no")
async def cancel_publish_event(callback_query: CallbackQuery, state: FSMContext):
    data = await state.update_data(em_id = callback_query.message.message_id+1)
    chat_id = callback_query.from_user.id
    bot = get_bot()
    on_delete = list(range(data["sm_id"],data["em_id"]))
    await bot.delete_messages(chat_id=chat_id,message_ids=on_delete)
    await state.clear()
    await callback_query.message.answer(
        text="Ви відмінили публікацію події.",
        reply_markup=back_to_main_admin()
    )