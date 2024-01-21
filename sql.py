import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `channels` (
            `channel_name` CHAR(30),
            `channel_id` CHAR(15)
        );""")
        self.connection.commit()

    def add_channel(self, channel_id, channel_name=''):
        self.cursor.execute(f"""INSERT INTO channels
        VALUES ({channel_name}, {channel_id})
        """)
