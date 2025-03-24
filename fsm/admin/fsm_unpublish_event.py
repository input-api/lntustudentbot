from aiogram.fsm.state import StatesGroup, State


class UnpublishEvent(StatesGroup):
    get_id_event = State()
    approve = State()
