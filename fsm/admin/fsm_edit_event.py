from aiogram.fsm.state import StatesGroup, State

class EditEvent(StatesGroup):
    get_id_event = State()
    get_param_for_change = State()
    set_photo = State()
    update_event = State()