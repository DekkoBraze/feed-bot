from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from sql import Database
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

username = config['telephon']['username']
api_id = config['telephon']['api_id']
api_hash = config['telephon']['api_hash']
user_id = int(config['telephon']['user_id'])
telephon_user_id = int(config['telephon']['telephon_user_id'])

database = Database('feed_bot.db')

client = TelegramClient(username, api_id, api_hash, system_version="4.16.30-vxCUSTOM_STRING")

last_media_group_id = ''


@client.on(events.NewMessage(user_id))
async def add_channel(event):
    try:
        if event.message.text == '/channels':
            channel_titles = '\n'.join([x[0] for x in database.get_channels()])
            await client.send_message(user_id, channel_titles)
        else:
            global last_media_group_id
            new_channel = await client.get_entity(
                event.message.fwd_from.from_id
            )
            if event.message.grouped_id != last_media_group_id or not event.message.grouped_id:
                last_media_group_id = event.message.grouped_id
                channel_ids = [int(x[1]) for x in database.get_channels()]
                if new_channel.id not in channel_ids:
                    database.add_channel(new_channel.title, new_channel.id)
                    await client(JoinChannelRequest(new_channel))
                    await client.send_message(user_id, 'Channel was successfully added!')
                else:
                    database.remove_channel(new_channel.id)
                    await client(LeaveChannelRequest(new_channel))
                    await client.send_message(user_id, 'Channel was removed!')
    except Exception as e:
        print(e)


@client.on(events.NewMessage())
async def forward_message(event):
    try:
        channel = await event.get_chat()
        channel_ids = [int(x[1]) for x in database.get_channels()]
        sender = await event.get_sender()
        if channel.id in channel_ids:
            await client.forward_messages(int(user_id), event.message, sender)
    except Exception as e:
        print(e)

client.start()
client.run_until_disconnected()
