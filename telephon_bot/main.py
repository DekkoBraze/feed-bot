from telethon import TelegramClient, events
import configparser
import json

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)
client.start()


@client.on(events.NewMessage(-1001916777851))
async def main(event):
    await client.forward_messages('me', event.message)

client.run_until_disconnected()
