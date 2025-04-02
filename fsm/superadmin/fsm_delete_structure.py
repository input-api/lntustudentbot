from aiogram.fsm.state import StatesGroup, State

class DeleteStructure(StatesGroup):
    get_id_structure = State()
    approve = State()