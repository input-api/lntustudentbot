from aiogram.fsm.state import StatesGroup, State

class AddAdmin(StatesGroup):
    position_title = State()
    tg_id = State()
    name = State()
    surname = State()
    phone = State()
    instagram = State()
    telegram = State()
    email = State()
    quote = State()
    structure = State()
    photo = State()