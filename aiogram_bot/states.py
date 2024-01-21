from aiogram.fsm.state import StatesGroup, State


class BotStates(StatesGroup):
    adding_channels = State()
