from aiogram.fsm.state import StatesGroup, State

class EditAdmin(StatesGroup):
    get_id_admin = State()
    select_param_edit = State()
    set_photo = State()
    update_admin = State()