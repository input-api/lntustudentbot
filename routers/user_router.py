from aiogram import F, Router, types
from aiogram.filters import Command

from sqlalchemy.ext.asyncio import AsyncSession

from db.orm_query import orm_update_status_event_notifications
from filters.main_filters import IsAdmin, IsSuperAdmin

from handlers.user_handlers.faculty_kbd_handler import faculty_router
from handlers.user_handlers.gov_kbd_handler import government_router
from handlers.user_handlers.hostel_opt_kbd_handler import hostel_option_router
from handlers.user_handlers.hostels_kbds_handler import hostels_router
from handlers.user_handlers.main_kbd_handler import main_menu_router
from handlers.user_handlers.add_question_fsm_handler import user_question_router

from kbds.admin.main_kbd import admin_keyboard
from kbds.superadmin.main_kbd import super_admin_keyboard
from kbds.user.main_kbd import main_keyboard, back_to_main
from kbds.user.hostel_opt_kbd import hostel_option_keyboard
from kbds.user.utils_kbds import yes_or_no_kbd

from views.user.views_government import view_gov_router
from views.user.views_government_faculty import view_gov_faculty_router
from views.user.views_government_hostels import view_gov_hostel_router

user_router = Router()
user_router.include_routers(
    main_menu_router,
    government_router,
    hostel_option_router,
    hostels_router,
    faculty_router,
    view_gov_router,
    view_gov_faculty_router,
    view_gov_hostel_router,
    user_question_router,
)

@user_router.message(Command('menu'))
async def menu(message: types.Message):
    await message.answer("Ось основна менюшка:", reply_markup=main_keyboard())

@user_router.message(Command('hostel'))
async def menu(message: types.Message):
    await message.answer("Якщо вас щось цікавить про гуртожиток, "
                         "ось що я можу запропонувати:", reply_markup=hostel_option_keyboard())

@user_router.message(Command('user_setting'))
async def menu(message: types.Message):
    await message.answer("Ви хочете отримувати сповіщення про події?", reply_markup=yes_or_no_kbd())

@user_router.callback_query(F.data == "back")
async def back(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text="Головне меню:",
        reply_markup=main_keyboard(),
    )

@user_router.callback_query(F.data == "event_notifications_yes")
async def set_event_notifications_on(callback_query: types.CallbackQuery, session: AsyncSession):
    uid = callback_query.from_user.id
    await orm_update_status_event_notifications(session=session, user_id=uid, status=True)
    await callback_query.message.edit_text(
        text="Сповіщення про події увімкнено! 🔔",
        reply_markup=back_to_main(),
    )

@user_router.callback_query(F.data == "event_notifications_no")
async def set_event_notifications_off(callback_query: types.CallbackQuery, session: AsyncSession):
    uid = callback_query.from_user.id
    await orm_update_status_event_notifications(session=session, user_id=uid, status=False)
    await callback_query.message.edit_text(
        text="Вам не надходитимуть сповіщення про події! 🔕",
        reply_markup=back_to_main(),
    )

@user_router.message(Command("admin"), IsAdmin())
async def admin(message: types.Message):
    await message.answer(
        text="Меню адміністратора:",
        reply_markup=admin_keyboard(True),
    )

@user_router.message(Command("sudo"), IsSuperAdmin())
async def super_admin(message: types.Message):
    await message.answer(
        text="Меню суперадміна:",
        reply_markup=super_admin_keyboard(),
    )