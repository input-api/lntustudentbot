from aiogram.fsm.state import StatesGroup, State

class ProposeIdea(StatesGroup):
    idea = State()
    from_whom_id = State()
    proposed_at = State()