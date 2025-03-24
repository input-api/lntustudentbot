from aiogram.fsm.state import StatesGroup, State

class DeleteEvent(StatesGroup):
    get_id_event = State()
    approve_delete = State()