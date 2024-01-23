from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

greet_menu = [
    [InlineKeyboardButton(text="Регистрация", callback_data="start_userbot_registration")]
]
greet_menu = InlineKeyboardMarkup(inline_keyboard=greet_menu)

menu = [
    [InlineKeyboardButton(text="Перейти в ленту", callback_data="get_feed"),
    InlineKeyboardButton(text="Добавить каналы", callback_data="add_channels")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)

add_channels_menu = [
    [InlineKeyboardButton(text="Завершить добавление", callback_data="complete_adding_channels")]
]
add_channels_menu = InlineKeyboardMarkup(inline_keyboard=add_channels_menu)
