import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `channels` (
            `channel_title` CHAR(50),
            `channel_id` CHAR(15) UNIQUE
        );""")
        self.connection.commit()

    def add_channel(self, channel_name, channel_id):
        self.cursor.execute(f"""INSERT INTO channels
        VALUES ('{channel_name}', '{channel_id}')
        """)
        self.connection.commit()

    def remove_channel(self, channel_id):
        self.cursor.execute(f"""DELETE FROM channels
        WHERE channel_id == '{channel_id}'
        """)
        self.connection.commit()

    def get_channels(self):
        self.cursor.execute(f"""SELECT *
                    FROM channels
                    """)
        return self.cursor.fetchall()
