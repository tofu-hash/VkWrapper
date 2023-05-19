from aiogram.dispatcher.filters.state import State, StatesGroup


class Settings(StatesGroup):
    set_openai_api_key = State()
    change_model = State()
