from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from bot import bot
from db.orm_query import orm_add_structure
from fsm.superadmin.fsm_add_structure import AddStructure
from kbds.superadmin.main_kbd import back_main_superadmin
from kbds.superadmin.structure_actions_kbd import StructureOptCbData, StructureOptActions

add_structure_router = Router()

@add_structure_router.callback_query(StructureOptCbData.filter(F.action == StructureOptActions.add_structure))
async def add_structure(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(sm_id=callback_query.message.message_id - 1)
    await state.set_state(AddStructure.full_name)
    await callback_query.message.edit_text(
        text="Введіть повну назву структури:",
    )

@add_structure_router.message(AddStructure.full_name, F.text)
async def handle_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(AddStructure.short_name)
    await message.answer(
        text="Введіть коротку назву структури:",
    )

@add_structure_router.message(AddStructure.full_name)
async def handle_full_name_invalid(message: Message):
    await message.answer(
        text="Введіть текстом назву структури.",
    )

@add_structure_router.message(AddStructure.short_name, F.text)
async def handle_short_name(message: Message, state: FSMContext, session: AsyncSession):
    short_name = message.text
    data = await state.update_data(short_name=short_name.casefold(), em_id = message.message_id+1)

    chat_id = message.from_user.id
    on_delete = list(range(data["sm_id"],data["em_id"]))
    await bot.delete_messages(chat_id=chat_id,message_ids=on_delete)

    await state.clear()
    await orm_add_structure(session, data)
    await message.answer(
        text=f"Дані збережено!\n\nПовна назва: {data["full_name"]}\nКоротка назва: {data["short_name"]}",
        reply_markup=back_main_superadmin()
    )

@add_structure_router.message(AddStructure.short_name)
async def handle_short_name_invalid(message: Message):
    await message.answer(
        text="Введіть текстом коротку назву структури.",
    )
