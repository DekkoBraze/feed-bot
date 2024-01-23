from sql import Database
import os
import configparser

path_to_user_data = os.path.dirname(__file__).replace('telephon_bot', 'user_data')


def get_login_data():
    config = configparser.ConfigParser()
    config.read(os.path.join(path_to_user_data, 'config.ini'))

    username = config['telephon']['username']
    api_id = config['telephon']['api_id']
    api_hash = config['telephon']['api_hash']

    return username, api_id, api_hash,


def get_database():
    database = Database(os.path.join(path_to_user_data, 'feed_bot.db'))

    return database


def get_bot_id():
    config = configparser.ConfigParser()
    config.read(os.path.join(path_to_user_data, 'config.ini'))
    bot_id = config['aiogram']['bot_id']

    return bot_id


def get_user_id():
    config = configparser.ConfigParser()
    config.read(os.path.join(path_to_user_data, 'config.ini'))
    user_id = config['aiogram']['user_id']

    return user_id