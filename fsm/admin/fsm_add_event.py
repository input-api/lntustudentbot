from aiogram.fsm.state import StatesGroup, State

class AddEvent(StatesGroup):
    title = State()
    description = State()
    date_start = State()
    time_start = State()
    location = State()
    organizer = State()
    image = State()
    approve = State()