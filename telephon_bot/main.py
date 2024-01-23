from telethon import TelegramClient, events, types
import configparser
import json
from telephon_bot.utils import get_login_data, get_bot_id
import asyncio
from utils import get_database, get_user_id
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

username, api_id, api_hash = get_login_data()
client = TelegramClient(username, api_id, api_hash)


async def register_userbot(phone, code, phone_code_hash):
    try:
        username, api_id, api_hash = get_login_data()
        client = TelegramClient(username, api_id, api_hash)
        await client.connect()
        await client.sign_in(phone, code, phone_code_hash=phone_code_hash)
        return True
    except Exception as e:
        print(e)
        return False


async def get_hash_code(phone):
    username, api_id, api_hash = get_login_data()
    client = TelegramClient(username, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        phone_code_hash = await client.send_code_request(phone)
        return phone_code_hash
    else:
        return "registered"


async def is_authorized():
    username, api_id, api_hash = get_login_data()
    client = TelegramClient(username, api_id, api_hash)
    await client.connect()
    if await client.is_user_authorized():
        return True
    else:
        return False


async def join_channels():
    username, api_id, api_hash = get_login_data()
    client = TelegramClient(username, api_id, api_hash)
    await client.connect()
    database = get_database()
    channels_lst = database.get_channels()
    for channel in channels_lst:
        print(channel[1])
        integer = int(channel[1])
        print(integer)
        channel_entity = await client.get_entity(integer)
        await client(JoinChannelRequest(channel_entity))


@client.on(events.NewMessage())
async def start_feeding(event):
    database = get_database()
    channels_lst = database.get_channels()
    bot_id = get_bot_id()
    user_id = get_user_id()
    sender = await event.get_sender()
    if event.chat_id == 486857274:
        print(event.message)
        await client.forward_messages(int(user_id), event.message, sender)
    #for channel in channels_lst:
    #    if channel[1] == event.chat_id:
    #        await client.forward_messages(int(bot_id), event.message)


async def start_feeding_loop():
    await client.connect()
    await client.run_until_disconnected()

#@client.on(events.NewMessage(-1001916777851))
#async def main(event):
#    username, api_id, api_hash = get_login_data()
#    client = TelegramClient(username, api_id, api_hash)
#    await client.connect()
#    bot_id = get_bot_id()
#    await client.forward_messages(bot_id, event.message)

#async def start_telephon(phone, code=''):
#    try:
#        username, api_id, api_hash = get_login_data()
#        client = TelegramClient(username, api_id, api_hash)
#        await client.connect()
#        #if not client.is_user_authorized():
#        #    await client.send_code_request(phone)
#        #    phone_code_hash = await client.send_code_request(phone).phone_code_hash
#        if code:
#            await client.sign_in(phone, code)
#        else:
#            try:
#                hash = await client.send_code_request(phone)
#            except Exception as e:
#                print(e)
#                print(hash)
#        return True
#    except Exception as e:
#        print(e)
#        return False

#Последняя версия:
#async def regisTEr_userbot(phone, phone_code_hash, code):
#    try:
#        username, api_id, api_hash = get_login_data()
#        client = TelegramClient(username, api_id, api_hash)
#        await client.connect()
#        await client.sign_in(phone, code, phone_code_hash=phone_code_hash)
#        return True
#    except Exception:
#        return False
#
#
#async def get_hash_code(phone):
#    username, api_id, api_hash = get_login_data()
#    client = TelegramClient(username, api_id, api_hash)
#    await client.connect()
#    if not await client.is_user_authorized():
#        await client.send_code_request(phone)
#        phone_code_hash = await client.send_code_request(phone)
#        print(phone_code_hash)
#        return phone_code_hash
#    else:
#        return "registered"


#client.run_until_disconnected()

#async def start_telephon(phone, code=''):
#    try:
#        username, api_id, api_hash = get_login_data()
#        client = TelegramClient(username, api_id, api_hash)
#        await client.connect()
#        if not client.is_user_authorized():
#            await client.send_code_request(phone)
#            phone_code_hash = await client.send_code_request(phone).phone_code_hash
#        if code:
#            await client.sign_in(phone, code)
#        else:
#            await client.sign_in(phone)
#        return True
#    except Exception:
#        return False