from aiogram.fsm.state import StatesGroup, State

class EditStructure(StatesGroup):
    get_id_structure = State()
    select_param_edit = State()
    approve = State()