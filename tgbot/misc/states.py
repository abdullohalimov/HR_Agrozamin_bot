from aiogram.dispatcher.filters.state import StatesGroup, State

class UserInfo(StatesGroup):
    # policy = State()
    fio = State()
    telefon = State()
    jins = State()
    age = State()
    education = State()
    prog_language = State()
    additional = State()
    resume = State()
    final = State()
    registered = State()