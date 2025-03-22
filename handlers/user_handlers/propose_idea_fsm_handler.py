from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from db.orm_query import orm_add_structure, orm_add_propose_idea
from fsm.user.fsm_propose_idea import ProposeIdea
from handlers.user_handlers.utils import dictionary_faculty_key
from kbds.user.main_kbd import back_to_main
from kbds.user.faculty_kbd import FacultyCbData

propose_idea_router = Router()

@propose_idea_router.callback_query(FacultyCbData.filter(F.previous_action == "propose_idea"))
async def propose_idea(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(ProposeIdea.idea)
    _, faculty, _ = callback_query.data.split(":")
    proposed_at = await dictionary_faculty_key(faculty)
    await state.update_data(proposed_at=proposed_at)
    await callback_query.message.edit_text(
        text="Що ви хочете запропонувати?",
    )

@propose_idea_router.message(ProposeIdea.idea, F.text)
async def handle_short_name(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.update_data(idea=message.text, from_whom_id=message.from_user.id)
    await state.clear()
    await orm_add_propose_idea(session, data)
    await message.answer(
        text=f"Ідею надіслано факультету!\n\nІдея: {data["idea"]}\nДля факультету: {data["proposed_at"]}",
        reply_markup=back_to_main()
    )

@propose_idea_router.message(ProposeIdea.idea)
async def handle_full_name_invalid(message: Message):
    await message.answer(
        text="Введіть текстом ідею яку хочетете запропонувати.",
    )

