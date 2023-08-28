import sqlite3


class Database:
    def __init__(self):
        self.connect_ = self.connect()
        self.cursor = self.connect_.cursor()
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS "messages" ("id"	INTEGER NOT NULL UNIQUE,'
                            f'"user_id"	INTEGER NOT NULL,'
                            f'"message_id"	INTEGER NOT NULL,'
                            f'"message_user"	TEXT,'
                            f'"message_bot"	TEXT,'
                            f'PRIMARY KEY("id" AUTOINCREMENT))')

    def connect(self):
        connection = sqlite3.connect('database.db')
        return connection

    def close(self):
        self.connect_.close()

    def add_context(self, user_id, message_id, message_user, message_bot):
        self.cursor.execute('INSERT INTO messages (user_id, message_id, message_user,message_bot) VALUES (?, ?, ?,?)',
                            (user_id, message_id, message_user, message_bot))
        self.connect_.commit()

    def get_context(self, user_id):
        ans = self.cursor.execute(f'SELECT message_user, message_bot FROM messages WHERE user_id = {user_id} '
                                  f'ORDER BY message_id DESC '
                                  f'LIMIT 2').fetchall()
        user_messages = [message[0] for message in ans]
        bot_messages = [message[1] for message in ans]
        return user_messages, bot_messages

    def delete_context(self, user_id):
        self.cursor.execute(f'DELETE FROM messages WHERE user_id = {user_id}')
        self.connect_.commit()
