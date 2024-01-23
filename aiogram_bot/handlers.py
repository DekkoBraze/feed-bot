from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
import kb
import text
from states import BotStates
from aiogram.fsm.context import FSMContext
from utils import get_database, get_users_id
from aiogram.types.callback_query import CallbackQuery
from telephon_bot.main import get_hash_code, register_userbot, is_authorized, start_feeding, join_channels, start_feeding_loop, stop_feeding_loop

router = Router()
media_group_ids = set()
phone_num = ''
code_hash = ''


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.greet_menu)


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
    #await join_channels()
    await state.clear()


@router.message(Command("channels"))
async def get_channels_list(msg: Message):
    database = get_database()
    channels_list = database.get_channels()
    await msg.answer(text=str(channels_list), reply_markup=kb.menu)


@router.callback_query(F.data == "start_userbot_registration")
async def start_userbot_registration(clbck: CallbackQuery, state: FSMContext):
    is_user_authorized = await is_authorized()
    if not is_user_authorized:
        await clbck.bot.send_message(clbck.message.chat.id, "Введите ваш номер телефона.")
        await state.set_state(BotStates.asking_phone)
    else:
        await clbck.bot.send_message(clbck.message.chat.id, "Вы уже зарегистрированы!")


@router.message(BotStates.asking_phone)
async def get_phone(msg: Message, state: FSMContext):
    global phone_num
    global code_hash
    phone_num = msg.text
    code_object = await get_hash_code(phone_num)
    if code_object == "registered":
        await msg.answer("Вы уже зарегистрированы!")
        await state.clear()
    elif code_object:
        code_hash = code_object.phone_code_hash
        await msg.answer("Введите код подтверждения")
        await state.set_state(BotStates.asking_code)
    else:
        await msg.answer(text.error_general)


@router.message(BotStates.asking_code)
async def get_code(msg: Message, state: FSMContext):
    code = int(msg.text)
    code += 1
    is_telephon_started = await register_userbot(phone_num, code, code_hash)
    if is_telephon_started:
        await msg.answer("Вы успешно зарегистрировались!")
        await state.clear()
    else:
        await msg.answer(text.error_general)


@router.callback_query(F.data == "get_feed")
async def get_feed(clbck: CallbackQuery, state: FSMContext):
    await clbck.bot.send_message(clbck.message.chat.id, "Лента успешно запущена! Чтобы закончить скроллинг, используйте команду exit.")
    await state.set_state(BotStates.feeding)
    await start_feeding_loop()


@router.message(Command('exit'), BotStates.feeding)
async def get_feed(msg: Message, state: FSMContext):
    await state.clear()
    await stop_feeding_loop()
    await msg.answer("Лента остановлена!", reply_markup=kb.menu)


@router.message(BotStates.feeding)
async def forward_messages(msg: Message, state: FSMContext):
    user_id, telephon_user_id = get_users_id()
    if msg.chat.id == int(telephon_user_id):
        print('feeding_in_proccess')
        await msg.forward(user_id)
