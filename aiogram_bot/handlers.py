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
media_group_ids = set()


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
    database = get_database()
    try:
        if msg.forward_origin.type == "channel":
            if msg.media_group_id not in media_group_ids:
                media_group_ids.add(msg.media_group_id)
                possible_exception = database.add_channel(msg.forward_origin.chat.id, msg.forward_origin.chat.title)
                if not possible_exception:
                    await msg.answer(f"Канал {msg.forward_origin.chat.title} добавлен."
                                     f" Добавьте еще, либо нажмите кнопку завершить.", reply_markup=kb.add_channels_menu)
                elif possible_exception == "IntegrityError":
                    await msg.answer(text.error_duplicate, reply_markup=kb.add_channels_menu)
                else:
                    await msg.answer(text.error_general, reply_markup=kb.add_channels_menu)
        else:
            await msg.answer('Сообщение переслано не из канала. Пожалуйста, повторите попытку.')
    except Exception:
        await msg.answer(text.error_general, reply_markup=kb.add_channels_menu)


@router.callback_query(F.data == "complete_adding_channels")
async def complete_adding_channels(clbck: CallbackQuery, state: FSMContext):
    media_group_ids.clear()
    await clbck.bot.send_message(clbck.message.chat.id, "Добавление завершено.", reply_markup=kb.menu)
    await state.clear()


@router.message(Command("channels"))
async def get_channels_list(msg: Message):
    database = get_database()
    channels_list = database.get_channels()
    await msg.answer(text=channels_list, reply_markup=kb.menu)
