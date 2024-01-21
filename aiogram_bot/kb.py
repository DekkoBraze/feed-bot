from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text="Перейти в ленту", callback_data="get_feed"),
    InlineKeyboardButton(text="Добавить каналы", callback_data="add_channels")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)

add_channels_menu = [
    [InlineKeyboardButton(text="Завершить добавление", callback_data="get_feed")]
]
add_channels_menu = InlineKeyboardMarkup(inline_keyboard=add_channels_menu)
