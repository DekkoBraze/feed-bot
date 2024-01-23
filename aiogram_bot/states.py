from aiogram.fsm.state import StatesGroup, State


class BotStates(StatesGroup):
    adding_channels = State()
    asking_phone = State()
    asking_code = State()
    feeding = State()
