## About

FeedBot is a Telegram bot that will help you organize many separate channels into a single beautiful feed.

> **To use this bot, you need to have two Telegram accounts (and two phone numbers, properly).**

## Installation

1. Install dependencies with requirements.txt:

```
pip install -r requirements.txt
```

or poetry:

```
poetry install
```

2. Set up Telephon ([documentation](https://docs.telethon.dev/en/stable/basic/signing-in.html)). When logging in with a terminal, use info of a secondary account - it will forward messages from channels to your main account.

3. Enter your data in config.ini (you have received *api_id* and *api_hash* after Telephon installation; you can find your main account *user_id* and your secondary account *telephon_user_id* with @userinfobot)

## How to use

You can add a channel to feed by forwarding a message from it to the secondary account (*telephon_user_id*). If channel is already in the database, forwarding a message will remove it from feed. To check up channels list, send '/channels'.

You will receive new posts from listed channels in the same dialogue.
