from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from sqlalchemy.ext.asyncio import AsyncSession

from db.orm_query import orm_add_position, orm_get_structure
from fsm.superadmin.fsm_add_admin import AddAdmin
from kbds.superadmin.admin_actions_kbd import AdminOptActions, AdminOptCbData
from kbds.superadmin.main_kbd import back_main_superadmin

add_admin_router = Router()

@add_admin_router.callback_query(AdminOptCbData.filter(F.action == AdminOptActions.add_admin))
async def add_admin(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(AddAdmin.position_title)
    await callback_query.message.edit_text(
        text="Введіть посаду адміна:",
    )

@add_admin_router.message(AddAdmin.position_title, F.text)
async def handle_position_title(message: Message, state: FSMContext):
    await state.update_data(position_title=message.text)
    await state.set_state(AddAdmin.tg_id)
    await message.answer(
        text="Перешліть повідомлення від користувача який займає цю посаду /n(для отримання tg_id).",
    )

@add_admin_router.message(AddAdmin.position_title)
async def handle_position_title_invalid(message: Message):
    await message.answer(
        text="Введіть текстом назву посади.",
    )

@add_admin_router.message(AddAdmin.tg_id, F.forward_from | F.forward_from_chat)
async def handle_tg_id(message: Message, state: FSMContext):
    await state.update_data(tg_id=message.forward_origin.sender_user.id, telegram=message.forward_origin.sender_user.username)
    await state.set_state(AddAdmin.name)
    await message.answer("Ім'я адміна")


@add_admin_router.message(AddAdmin.tg_id)
async def handle_tg_id_invalid(message: Message):
    await message.answer(
        "Повідомлення не переслане від користувача або в нього прихований профіль. \n "
        "Попросіть відкрити профіль в налаштуваннях та перешліть ще раз."
    )

@add_admin_router.message(AddAdmin.name, F.text)
async def handle_name_admin(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddAdmin.surname)
    await message.answer("Прізвище адміна")

@add_admin_router.message(AddAdmin.name)
async def handle_name_admin_invalid(message: Message):
    await message.answer(
        text="Введіть текстом ім'я адміна.",
    )

@add_admin_router.message(AddAdmin.surname, F.text)
async def handle_surname_admin(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(AddAdmin.phone)
    await message.answer("Номер телефону адміна/n"
                         "Формат: +380XXXXXXXXX")

@add_admin_router.message(AddAdmin.surname)
async def handle_surname_admin_invalid(message: Message):
    await message.answer(
        text="Введіть текстом прізвище адміна.",
    )

@add_admin_router.message(AddAdmin.phone, F.text.regexp(r"^\+380\d{9}$"))
async def handle_phone_admin(message: Message, state: FSMContext):
    await state.update_data(phone=str(message.text))
    await state.set_state(AddAdmin.instagram)
    await message.answer("Ваш нік в інстаграм")

@add_admin_router.message(AddAdmin.phone)
async def handle_phone_admin_invalid(message: Message):
    await message.answer(
        text="Введіть телефон правильним форматом +380XXXXXXXXX",
    )

@add_admin_router.message(AddAdmin.instagram, F.text)
async def handle_instagram_and_telegram_admin(message: Message, state: FSMContext):
    await state.update_data(instagram=message.text)
    await state.set_state(AddAdmin.email)
    await message.answer("Введіть електронну адресу")

@add_admin_router.message(AddAdmin.instagram)
async def handle_instagram_admin_invalid(message: Message):
    await message.answer(
        text="Введіть нік текстом",
    )

@add_admin_router.message(AddAdmin.email, F.text.regexp(r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"))
async def handle_email_admin(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(AddAdmin.quote)
    await message.answer("Введіть цитату")

@add_admin_router.message(AddAdmin.email)
async def handle_email_admin_invalid(message: Message):
    await message.answer(
        text="Введіть коректний емейл",
    )

@add_admin_router.message(AddAdmin.quote, F.text)
async def handle_quote_admin(message: Message, state: FSMContext):
    await state.update_data(quote=message.text)
    await state.set_state(AddAdmin.structure)
    await message.answer("Введіть скорочену назву структури до якої належить посада(Загал, ФКІТ, Гурт №1)")

@add_admin_router.message(AddAdmin.quote)
async def handle_quote_admin_invalid(message: Message):
    await message.answer(
        text="Введіть цитату текстом",
    )

@add_admin_router.message(AddAdmin.structure, F.text)
async def handle_structure_admin(message: Message, state: FSMContext, session: AsyncSession):
    short_name = message.text
    structure = short_name.casefold()
    data = await orm_get_structure(session, structure)
    if data:
        await state.update_data(structure=structure)
        await state.set_state(AddAdmin.photo)
        await message.answer("Надішліть фото адміна")

    else:
        await state.set_state(AddAdmin.structure)
        await message.answer("Структури не знайдено. Перевірте написання або створіть нову.")


@add_admin_router.message(AddAdmin.structure)
async def handle_structure_admin_invalid(message: Message):
    await message.answer(
        text="Введіть скорочену назву структури",
    )

@add_admin_router.message(AddAdmin.photo, F.photo)
async def handle_photo_admin(message: Message, state: FSMContext, session: AsyncSession()):
    photo = message.photo[-1]
    file_id = photo.file_id
    data = await state.update_data(photo_file_id=file_id)
    await state.clear()
    await orm_add_position(session, data)
    await message.answer(text=f"Дані збережено!", reply_markup=back_main_superadmin())

@add_admin_router.message(AddAdmin.photo)
async def handle_photo_admin_invalid(message: Message):
    await message.answer(
        text="Надішліть фото",
    )


@add_admin_router.message(StateFilter("*"), F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    curent_state = await state.get_state()
    if curent_state is None:
        return

    await state.clear()
    await message.answer("Дії відмінено!", reply_markup=back_main_superadmin())