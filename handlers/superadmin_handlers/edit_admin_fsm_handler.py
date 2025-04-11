import re

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from bot import bot
from db.orm_query import orm_get_all_positions, orm_get_positions_id_list, orm_update_position_photo, \
    orm_update_position
from fsm.superadmin.fsm_edit_admin import EditAdmin
from kbds.superadmin.admin_actions_kbd import AdminOptCbData, AdminOptActions
from kbds.superadmin.main_kbd import back_main_superadmin

edit_admin_router = Router()

@edit_admin_router.callback_query(AdminOptCbData.filter(F.action == AdminOptActions.edit_admin))
async def edit_admin(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    positions = await orm_get_all_positions(session)
    if not positions:
        await callback_query.message.edit_text(
            text="Ви ще не додали адміністраторів.",
            reply_markup=back_main_superadmin()
        )

    else:
        text = "\n".join([f"🆔:{position.id} - {position.position_title}" for position in positions])
        await state.update_data(sm_id=callback_query.message.message_id - 1)
        await state.set_state(EditAdmin.get_id_admin)
        await callback_query.message.edit_text(
            text=f"{text}\n\n"
                 "Введіть id адміна, якого хочете редагувати:",
        )

@edit_admin_router.message(EditAdmin.get_id_admin, F.text)
async def get_id_admin_for_edit(message: Message, session: AsyncSession, state: FSMContext):
    position_list_id = await orm_get_positions_id_list(session)
    position_id = int(message.text)

    if position_id in position_list_id:
        await state.update_data(position_id = position_id)
        await state.set_state(EditAdmin.select_param_edit)
        await message.answer(
            text="Введіть параметр для редагування:\n"
                 "назва, тгід, ім'я, прізвище, телефон, інстаграм, телеграм, емейл, цитата, адмін-статус, фото",
        )
    else:
        await state.set_state(EditAdmin.get_id_admin)
        await message.answer(
            text="Не коректний id або адміна не існує. Спробуйте знову!",
        )

@edit_admin_router.message(EditAdmin.select_param_edit, F.text)
async def get_param_admin_for_edit(message: Message, state: FSMContext):
    param = ""
    param_text = message.text
    match param_text.lower():
        case "назва":
            param = "position_title"
        case "тгід":
            param = "tg_id"
        case "ім'я":
            param = "name"
        case "прізвище":
            param = "surname"
        case "телефон":
            param = "phone"
        case "інстаграм":
            param = "instagram"
        case "телеграм":
            param = "telegram"
        case "емейл":
            param = "email"
        case "цитата":
            param = "quote"
        case "адмін-статус":
            param = "is_admin"
        case "фото":
            await state.set_state(EditAdmin.set_photo)
            await message.answer(
                text="Надішліть нове фото:"
            )
            return
        case _:
            await state.set_state(EditAdmin.select_param_edit)
            await message.answer(
                text="Не коректний параметр. Спробуйте знову."
            )
            return

    await state.update_data(param=param)
    await state.set_state(EditAdmin.update_admin)
    await message.answer(
        "Введіть нове значення:"
    )

@edit_admin_router.message(EditAdmin.set_photo, F.photo)
async def set_new_admin_photo(message: Message, session: AsyncSession, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    data = await state.get_data()
    position_id = data["position_id"]

    user_id = message.from_user.id
    em_id = message.message_id+1
    on_delete = list(range(data["sm_id"], em_id))
    await bot.delete_messages(chat_id=user_id, message_ids=on_delete)

    await state.clear()
    await orm_update_position_photo(session, position_id, file_id)
    await message.answer(
        text="Фото оновлено.",
        reply_markup=back_main_superadmin()
    )

@edit_admin_router.message(EditAdmin.set_photo)
async def set_new_admin_photo_invalid(message: Message):
    await message.answer(
        text="Надішліть фото.",
    )

@edit_admin_router.message(EditAdmin.update_admin, F.text)
async def update_admin(message: Message, session: AsyncSession, state: FSMContext):
    value = message.text
    data = await state.update_data(updated_data = value)
    param = data["param"]
    position_id = data["position_id"]
    error = False

    text = "Адміна оновлено"

    match param:
        case "position_title":
            if not isinstance(value, str) or not value:
                error = True
                text = "Некоректна посада. Перегляньте та спробуйте ще раз."
        case "tg_id":
            if not message.forward_origin or not getattr(message.forward_origin, "sender_user", None):
                error = True
                text = (
                    "Повідомлення не переслане від користувача або в нього прихований профіль. \n"
                    "Попросіть відкрити профіль в налаштуваннях та перешліть ще раз."
                )
            else:
                value = message.forward_origin.sender_user.id
        case "name":
            if not isinstance(value, str) or not value:
                error = True
                text = "Введіть текстом ім'я адміна."
        case "surname":
            if not isinstance(value, str) or not value:
                error = True
                text = "Введіть текстом прізвище адміна."
        case "phone":
            if not re.match(r"^\+380\d{9}$", value):
                error = True
                text = "Введіть телефон правильним форматом +380XXXXXXXXX."
        case "instagram":
            if not isinstance(value, str) or not value:
                error = True
                text = "Введіть коректне посилання на інстаграм."
        case "telegram":
            if not message.forward_origin or not getattr(message.forward_origin, "sender_user", None):
                error = True
                text = (
                    "Повідомлення не переслане від користувача або в нього прихований профіль. \n"
                    "Попросіть відкрити профіль в налаштуваннях та перешліть ще раз."
                )
            else:
                value = message.forward_origin.sender_user.username
        case "email":
            if not re.match(r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$", value):
                error = True
                text = "Введіть коректний емейл."
        case "quote":
            if not isinstance(value, str) or not value:
                error = True
                text = "Введіть цитату текстом."
        case "is_admin":
            if value.lower() not in ['+', "yes", "y", "так", '-', "no", "n", "ні"]:
                error = True
                text = ("Введіть значення текстом.\n"
                        '"+", "yes", "y", "так", "-", "no", "n", "ні"')
            elif value.lower() in ['+', "yes", "y", "так"]:
                value = True
            else:
                value = False

    if error:
        await state.set_state(EditAdmin.update_admin)
        await message.answer(text=text)
        return
    else:
        await orm_update_position(session, position_id=position_id, **{param: value})

    user_id = message.from_user.id
    em_id = message.message_id+1
    on_delete = list(range(data["sm_id"], em_id))
    await bot.delete_messages(chat_id=user_id, message_ids=on_delete)

    await message.answer(
        text=text,
        reply_markup=back_main_superadmin()
    )
