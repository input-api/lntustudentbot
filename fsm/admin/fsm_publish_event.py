from aiogram.fsm.state import StatesGroup, State

class PublishEvent(StatesGroup):
    get_id_event = State()
    approve = State()
