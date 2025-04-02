from aiogram import F, Router
from aiogram.types import CallbackQuery, InputMediaPhoto

from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from bot_setup import get_bot
from db.orm_query import orm_get_positions, orm_get_image_by_position_id
from handlers.user_handlers.utils import dictionary_faculty_key
from kbds.user.gov_kbd import GovCbData, GovActions
from kbds.user.hostels_kbds import HostelsCbData
from kbds.user.main_kbd import main_keyboard

view_gov_hostel_router = Router()

@view_gov_hostel_router.callback_query(HostelsCbData.filter(F.previous_action == "gov"))
async def show_student_hostels_government(callback_query: CallbackQuery, session: AsyncSession):
    hostel = callback_query.data.split(":")[1]
    structure = str(await dictionary_faculty_key(hostel))
    datas = await orm_get_positions(session, structure)
    if not datas:
        await callback_query.answer("Дані відсутні.", show_alert=True)
        return

    await send_hostels_government_page(callback_query, session, datas, structure, index=0)


async def send_hostels_government_page(callback_query: CallbackQuery, session: AsyncSession, datas, structure, index: int):
    data = datas[index]
    img = await orm_get_image_by_position_id(session, data.id)
    total = len(datas)

    builder = InlineKeyboardBuilder()

    navigation_buttons = []
    if index > 0:
        navigation_buttons.append(("⬅️ " + datas[index - 1].position_title.split(" ")[0], f"{structure}_faculty-gov_{index - 1}"))
    if index < total - 1:
        navigation_buttons.append((datas[index + 1].position_title.split(" ")[0] + " ➡️", f"{structure}_faculty-gov_{index + 1}"))

    for text, callback in navigation_buttons:
        builder.button(text=text, callback_data=callback)

    builder.button(text="🏡 Головне меню", callback_data="back_to_main_from_faculty_gov")

    if len(navigation_buttons) == 2:
        builder.adjust(2, 1)
    else:
        builder.adjust(1)

    caption_text = (
        f"<b>{data.position_title}</b>\n"
        f"👤 {data.name} {data.surname}\n"
        f"📞 Телефон: {data.phone}\n"
        f"📱 Instagram: {data.instagram if data.instagram else 'Не вказано'}\n"
        f"📲 Telegram: {data.telegram if data.telegram else 'Не вказано'}\n"
        f"✉️ Email: {data.email if data.email else 'Не вказано'}\n"
        f"📝 Цитата: {data.quote if data.quote else 'Без опису'}"
    )

    await callback_query.message.edit_media(
        media=InputMediaPhoto(media=img.image, caption=caption_text, parse_mode="HTML"),
        reply_markup=builder.as_markup()
    )



@view_gov_hostel_router.callback_query(F.data.contains("_faculty-gov_"))
async def paginate_government(callback_query: CallbackQuery, session: AsyncSession):
    split = callback_query.data.split("_")
    index = int(split[2])
    structure = str(split[0])
    datas = await orm_get_positions(session, structure)

    await send_hostels_government_page(callback_query, session, datas, structure, index)


@view_gov_hostel_router.callback_query(F.data == "back_to_main_from_faculty_gov")
async def back_to_main_from_gen_gov(callback_query: CallbackQuery):
    chat_id = callback_query.from_user.id
    bot = get_bot()
    on_delete = callback_query.message.message_id
    await bot.delete_message(chat_id=chat_id, message_id=on_delete)
    await callback_query.message.answer(
        text="Головне меню:",
        reply_markup=main_keyboard(),
    )