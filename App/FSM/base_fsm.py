from aiogram.fsm.state import State, StatesGroup


class Chat(StatesGroup):
    active_chat = State()
    generate_image = State()