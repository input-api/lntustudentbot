from aiogram.fsm.state import StatesGroup, State

class DeleteAdmin(StatesGroup):
    get_id_structure = State()
    approve = State()