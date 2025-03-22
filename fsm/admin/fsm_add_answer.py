from aiogram.fsm.state import StatesGroup, State

class AddAnswer(StatesGroup):
    select_question = State()
    set_answer = State()
    approve = State()