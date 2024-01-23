from sql import Database
import os
import configparser

path_to_user_data = os.path.dirname(__file__).replace('aiogram_bot', 'user_data')


def get_database():
    database = Database(os.path.join(path_to_user_data, 'feed_bot.db'))

    return database


def get_bot_token():
    config = configparser.ConfigParser()
    config.read(os.path.join(path_to_user_data, 'config.ini'))
    bot_token = config['aiogram']['bot_token']

    return bot_token


def get_user_id():
    config = configparser.ConfigParser()
    config.read(os.path.join(path_to_user_data, 'config.ini'))
    user_id = config['aiogram']['user_id']

    return user_id

#@router.channel_post()
#async def cp_handler(post: types.Message):
#    if post.sender_chat.title != config.CHANNEL_NAME:
#        return
#
#    await post.bot.forward_message(chat_id=config.USER_ID, from_chat_id=post.sender_chat.id, message_id=post.message_id)