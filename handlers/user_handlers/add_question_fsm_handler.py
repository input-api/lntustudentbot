from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import  AsyncSession

from db.orm_query import orm_add_question
from fsm.user.fsm_add_question import AddQuestion
from handlers.user_handlers.utils import dictionary_faculty_key
from kbds.user.faculty_kbd import FacultyCbData, FacultyActions
from kbds.user.main_kbd import back_to_main

user_question_router = Router()

@user_question_router.callback_query(FacultyCbData.filter(F.previous_action == "question"))
async def ask_user_question(callback_query: CallbackQuery, state: FSMContext):
    _, faculty, _ = callback_query.data.split(":")

    await state.update_data(
        for_whom=str(await dictionary_faculty_key(faculty)),
        from_whom_id=callback_query.from_user.id,
    )

    await state.set_state(AddQuestion.waiting_for_question)

    await callback_query.message.answer(text="✍ Введіть ваше питання:")


@user_question_router.message(AddQuestion.waiting_for_question)
async def receive_user_question(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    data["content"] = message.text
    data["message_id"] = message.message_id

    await orm_add_question(session=session, data=data)

    await message.answer(
        text="✅ Ваше питання надіслано!",
        reply_markup=back_to_main()
    )
    await state.clear()