from re import search

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from bot_setup import get_bot
from db.orm_query import orm_get_structure_by_tg_id_position, orm_get_questions, orm_add_answer, orm_get_from_whom_id
from fsm.admin.fsm_add_answer import AddAnswer
from handlers.admin_handlers.utils import approve
from kbds.admin.main_kbd import AdminCbData, AdminActions, back_to_main_admin

admin_answer_router = Router()

QUESTIONS_PER_PAGE = 5

@admin_answer_router.callback_query(AdminCbData.filter(F.action == AdminActions.questions))
async def show_user_questions(callback_query: CallbackQuery, session: AsyncSession, state: FSMContext, page: int = 0,):
    await state.update_data(sm_id = callback_query.message.message_id - 1)
    await state.set_state(AddAnswer.select_question)
    tg_id = callback_query.from_user.id
    structure = await orm_get_structure_by_tg_id_position(session=session, tg_id=tg_id)
    structure_short_name = structure.short_name
    questions = await orm_get_questions(session=session, structure=structure_short_name)

    if not questions:
        await callback_query.answer("Питання відсутні.")
        return

    start_index = page * QUESTIONS_PER_PAGE
    end_index = start_index + QUESTIONS_PER_PAGE
    current_questions = questions[start_index:end_index]
    builder = InlineKeyboardBuilder()
    builder.button(text="➡ Далі", callback_data=f"questions_next_{page + 1}")

    num_q = 1
    for q in current_questions:
        if num_q == QUESTIONS_PER_PAGE:
            await callback_query.message.answer(f"🆔:{q.id}\n❓{q.content}", reply_markup=builder.as_markup())
            break
        else:
            num_q = num_q + 1
            await callback_query.message.answer(f"🆔:{q.id}\n❓{q.content}")


@admin_answer_router.callback_query(F.data.startswith("questions_next_"))
async def paginate_questions(callback_query: CallbackQuery, session: AsyncSession, state: FSMContext):
    text = callback_query.message.text
    await callback_query.message.edit_text(text=text)
    page = int(callback_query.data.split("_")[-1])
    await show_user_questions(callback_query, session, state, page)
    await state.set_state(AddAnswer.select_question)

@admin_answer_router.message(AddAnswer.select_question)
async def select_answer(message: Message, state: FSMContext):
    # Перевіряємо, чи повідомлення є відповіддю на інше
    if message.reply_to_message:
        id = search(r"🆔:(\d+)", message.reply_to_message.text)
        parsed_id = id.group(1)
        if id:
            await message.answer("Введіть відповідь на питання:")
            await state.update_data(question_id=int(parsed_id), q_content = message.reply_to_message.text)
            await state.set_state(AddAnswer.set_answer)
        else:
            await message.answer("Дайте відповідь на питання яке має 🆔!")
            await state.set_state(AddAnswer.select_question)
    else:
        await message.answer("Оберіть питання, на яке хочете відповісти.")
        await state.set_state(AddAnswer.select_question)

@admin_answer_router.message(AddAnswer.set_answer, F.text)
async def set_answer(message: Message, state: FSMContext):
    data = await state.update_data(answer_text=message.text)
    await state.set_state(AddAnswer.approve)
    text = f"{data["q_content"]}\n\nВаша відповідь:\n{data["answer_text"]}"
    await message.answer(
        text=f"{text}\nПерегляньте написану відповідь та підтвердіть.",
        reply_markup=approve("add_answer")
    )

@admin_answer_router.callback_query(AddAnswer.approve, F.data == "add_answer_yes")
async def save_answer(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.update_data(who_answered_id=callback_query.from_user.id, em_id = callback_query.message.message_id)
    bot = get_bot()
    await orm_add_answer(session, data)
    user_id, content = await orm_get_from_whom_id(session, data["question_id"])

    on_delete = list(range(data["sm_id"], data["em_id"]))
    await bot.delete_messages(chat_id=user_id, message_ids=on_delete)

    await state.clear()
    await bot.send_message(
        chat_id=user_id,
        text=f"<blockquote>Ви питали:\n{content}</blockquote>\nВідповідь:\n{data["answer_text"]}"
    )
    await callback_query.message.edit_text(
        "Дані збережено"
    )

@admin_answer_router.callback_query(AddAnswer.approve, F.data == "add_answer_no")
async def cancel_answer(callback_query: CallbackQuery, state: FSMContext):
    data = await state.update_data(em_id = callback_query.message.message_id)
    chat_id = callback_query.from_user.id
    bot = get_bot()
    on_delete = list(range(data["sm_id"],data["em_id"]))
    await bot.delete_messages(chat_id=chat_id,message_ids=on_delete)
    await state.clear()
    await callback_query.message.edit_text(
        text="Ви відмінили збереження відповіді.",
        reply_markup=back_to_main_admin()
    )