from aiogram.fsm.state import StatesGroup, State

class AddQuestion(StatesGroup):
    waiting_for_question = State()
