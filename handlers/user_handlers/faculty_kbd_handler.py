from aiogram import F, Router
from aiogram.types import CallbackQuery

from kbds.user.faculty_kbd import FacultyCbData, FacultyActions
from kbds.user.main_kbd import back_to_main

faculty_router = Router()

# @faculty_router.callback_query(FacultyCbData.filter(F.action == FacultyActions.fmmt))
# async def settle_in_hostel(callback_query: CallbackQuery):
#     state, faculty, previous_action = callback_query.data.split(":")
#     await callback_query.message.edit_text(
#         text=f"Ви обрали факультет - {faculty} в дії - {previous_action}",
#         reply_markup=back_to_main()
#     )
#
# @faculty_router.callback_query(FacultyCbData.filter(F.action == FacultyActions.fbp))
# async def settle_in_hostel(callback_query: CallbackQuery):
#     state, faculty, previous_action = callback_query.data.split(":")
#     await callback_query.message.edit_text(
#         text=f"Ви обрали факультет - {faculty} в дії - {previous_action}",
#         reply_markup=back_to_main()
#     )
#
# @faculty_router.callback_query(FacultyCbData.filter(F.action == FacultyActions.ftsost))
# async def settle_in_hostel(callback_query: CallbackQuery):
#     state, faculty, previous_action = callback_query.data.split(":")
#     await callback_query.message.edit_text(
#         text=f"Ви обрали факультет - {faculty} в дії - {previous_action}",
#         reply_markup=back_to_main()
#     )
#
# @faculty_router.callback_query(FacultyCbData.filter(F.action == FacultyActions.ftmi))
# async def settle_in_hostel(callback_query: CallbackQuery):
#     state, faculty, previous_action = callback_query.data.split(":")
#     await callback_query.message.edit_text(
#         text=f"Ви обрали факультет - {faculty} в дії - {previous_action}",
#         reply_markup=back_to_main()
#     )
#
# @faculty_router.callback_query(FacultyCbData.filter(F.action == FacultyActions.fate))
# async def settle_in_hostel(callback_query: CallbackQuery):
#     state, faculty, previous_action = callback_query.data.split(":")
#     await callback_query.message.edit_text(
#         text=f"Ви обрали факультет - {faculty} в дії - {previous_action}",
#         reply_markup=back_to_main()
#     )
#
# @faculty_router.callback_query(FacultyCbData.filter(F.action == FacultyActions.fabd))
# async def settle_in_hostel(callback_query: CallbackQuery):
#     state, faculty, previous_action = callback_query.data.split(":")
#     await callback_query.message.edit_text(
#         text=f"Ви обрали факультет - {faculty} в дії - {previous_action}",
#         reply_markup=back_to_main()
#     )
#
# @faculty_router.callback_query(FacultyCbData.filter(F.action == FacultyActions.general_gov))
# async def settle_in_hostel(callback_query: CallbackQuery):
#     state, faculty, previous_action = callback_query.data.split(":")
#     await callback_query.message.edit_text(
#         text=f"Ви обрали факультет - {faculty} в дії - {previous_action}",
#         reply_markup=back_to_main()
#     )
#
# @faculty_router.callback_query(FacultyCbData.filter(F.action == FacultyActions.profcom))
# async def settle_in_hostel(callback_query: CallbackQuery):
#     state, faculty, previous_action = callback_query.data.split(":")
#     await callback_query.message.edit_text(
#         text=f"Ви обрали факультет - {faculty} в дії - {previous_action}",
#         reply_markup=back_to_main()
#     )