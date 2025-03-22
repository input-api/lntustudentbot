from aiogram.fsm.state import StatesGroup, State

class AddStructure(StatesGroup):
    full_name = State()
    short_name = State()