from datetime import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from bot import bot
from db.orm_query import orm_add_scheduled_event
from handlers.admin_handlers.utils import approve
from kbds.admin.main_kbd import back_to_main_admin
from kbds.admin.event_kbd import EventCbData, EventActions
from fsm.admin.fsm_add_event import AddEvent
add_event_router = Router()

@add_event_router.callback_query(EventCbData.filter(F.action == EventActions.add_event))
async def admin_add_event(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(sm_id = callback_query.message.message_id)
    await state.set_state(AddEvent.title)
    await callback_query.message.edit_text(
        text="Введіть заголовок події:",
    )

@add_event_router.message(AddEvent.title, F.text)
async def set_event_title(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    await state.set_state(AddEvent.description)
    await message.answer(
        text="Впишіть опис події:",
    )

@add_event_router.message(AddEvent.title)
async def set_event_title_invalid(message: Message):
    await message.answer(
        text="Впишіть коректно заголовок події.",
    )

@add_event_router.message(AddEvent.description, F.text)
async def set_event_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddEvent.date_start)
    await message.answer(
        text="Дата події:",
    )

@add_event_router.message(AddEvent.description)
async def set_event_description_invalid(message: Message):
    await message.answer(
        text="Впишіть коректно опис події.",
    )

@add_event_router.message(AddEvent.date_start, F.text.regexp(r"(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0,1,2])\.(19|20)\d{2}"))
async def set_event_date(message: Message, state: FSMContext):
    await state.update_data(date_start=message.text)
    await state.set_state(AddEvent.time_start)
    await message.answer(
        text="Час події:",
    )

@add_event_router.message(AddEvent.date_start)
async def set_event_date_start_invalid(message: Message):
    await message.answer(
        text="Впишіть дату за форматом DD.MM.YYYY, або перегляньте можливо ви ввели неіснуючу дату.",
    )


@add_event_router.message(AddEvent.time_start, F.text.regexp(r"^(?:([01][0-9]|2[0-3]):([0-5][0-9]))$"))
async def set_event_time(message: Message, state: FSMContext):
    await state.update_data(time_start=message.text)
    await state.set_state(AddEvent.location)
    await message.answer(
        text="Місце події:",
    )

@add_event_router.message(AddEvent.time_start)
async def set_event_time_start_invalid(message: Message):
    await message.answer(
        text="Впишіть час за форматом HH:MM, або перегляньте можливо ви ввели неіснуючий час.",
    )

@add_event_router.message(AddEvent.location, F.text)
async def set_event_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(AddEvent.organizer)
    await message.answer(
        text="Організатор(и) події:",
    )

@add_event_router.message(AddEvent.location)
async def set_event_location_invalid(message: Message):
    await message.answer(
        text="Впишіть коректно локацію.",
    )

@add_event_router.message(AddEvent.organizer, F.text)
async def set_event_organizer(message: Message, state: FSMContext):
    await state.update_data(organizer=message.text)
    await state.set_state(AddEvent.image)
    await message.answer(
        text="Фото-афіша події:",
    )

@add_event_router.message(AddEvent.organizer)
async def set_event_organizer_invalid(message: Message):
    await message.answer(
        text="Впишіть коректно організатора.",
    )

@add_event_router.message(AddEvent.image, F.photo)
async def set_event_image(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id

    data = await state.update_data(image=file_id)

    caption_text = (
        f"<b>{data["title"]}</b>\n\n"
        f"📅Дата: {data["date_start"]}\n"
        f"🕘Час: {data["time_start"]}\n"
        f"📍Локація: {data["location"]}\n"
        f"🧑‍💼Організатор: {data["organizer"]}\n\n"
        f"{data["description"]}\n\n"
        f"Ви підтверджуєте створення події?"
    )

    await state.set_state(AddEvent.approve)
    await message.answer_photo(
        photo=file_id,
        caption=caption_text,
        parse_mode="HTML",
        reply_markup=approve("add_event")
    )

@add_event_router.message(AddEvent.image)
async def set_event_image_invalid(message: Message):
    await message.answer(
        text="Надішліть фото.",
    )

@add_event_router.callback_query(AddEvent.approve, F.data == "add_event_yes")
async def save_event(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    user_id = callback_query.from_user.id
    data = await state.update_data(created_by=user_id, em_id = callback_query.message.message_id+1)
    datetime_str = f"{data['date_start']} {data['time_start']}"
    data["date_time"] = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")

    await orm_add_scheduled_event(session, data)

    on_delete = list(range(data["sm_id"], data["em_id"]))
    await bot.delete_messages(chat_id=user_id, message_ids=on_delete)

    await state.clear()
    await callback_query.message.answer(
        "Подія збережена.\n"
        "Перейдіть за наступним шляхом, щоб опублікувати подію:\n\n"
        "Основне меню адміністратора ➡️ Події ➡️ Мої події ➡️ Не опубліковані",
        reply_markup=back_to_main_admin()
    )

@add_event_router.callback_query(AddEvent.approve, F.data == "add_event_no")
async def cancel_event(callback_query: CallbackQuery, state: FSMContext):
    data = await state.update_data(em_id = callback_query.message.message_id+2)
    chat_id = callback_query.from_user.id
    on_delete = list(range(data["sm_id"],data["em_id"]))
    await bot.delete_messages(chat_id=chat_id,message_ids=on_delete)
    await state.clear()
    await callback_query.message.answer(
        text="Ви відмінили збереження події.",
        reply_markup=back_to_main_admin()
    )