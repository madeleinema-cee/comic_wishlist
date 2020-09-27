import sqlite3


class Db:
    def __init__(self, database):
        self.conn = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.conn.row_factory = sqlite3.Row

    def execute(self, query):
        self.cursor.execute(query)

    def fetchall(self, query):
        self.cursor = self.conn.cursor()
        self.execute(query)
        result = [dict(row) for row in self.cursor.fetchall()]
        return result

    def close(self):
        self.conn.close()






