from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
import kb
import text
from states import BotStates
from aiogram.fsm.context import FSMContext
from utils import get_database
from aiogram.types.callback_query import CallbackQuery

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(F.text == "Меню")
@router.message(Command("menu"))
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)


@router.callback_query(F.data == "add_channels")
async def add_channels(clbck: CallbackQuery, state: FSMContext):
    await clbck.bot.send_message(clbck.message.chat.id, text.add_channels, reply_markup=kb.add_channels_menu)
    await state.set_state(BotStates.adding_channels)


@router.message(BotStates.adding_channels)
async def set_channels(msg: Message, state: FSMContext):
    #database = get_database()
    print(msg.text)
    print(msg.forward_from_chat.title)
    #if msg.sender_chat.type == "channel":
    #    database.add_channel(msg.sender_chat.id, msg.sender_chat.full_name)
    #else:
    #    await msg.answer('Сообщение переслано не из канала. Пожалуйста, повторите попытку.')

