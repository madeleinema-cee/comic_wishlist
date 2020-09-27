from db import Db
import os


class SQLFileParser:
    def __init__(self, sql_path):
        db_path = 'comic_wishlist.db'
        os.remove(db_path)
        self.db = Db(db_path)
        self.database = 'comics'
        self.sql_path = sql_path
        self.intermediary_file = '/tmp/int.txt'
        self.unwanted_lines = ['--']
        self.queries = []

    def main(self):
        with open(self.sql_path, encoding='utf-16') as f, open(self.intermediary_file, 'w+') as i:
            for line in f:
                if line[0:2] not in self.unwanted_lines:
                    i.write(line.strip('\r\n'))

        with open(self.intermediary_file, mode='r+', encoding='utf-8-sig') as i:
            self.queries = i.read().split(';GO')

        for q in self.queries:
            if q[0:5] != 'ALTER':
                q = self.replace(q)
                self.db.cursor.execute(q)

        self.db.conn.commit()

    @staticmethod
    def replace(q):
        return q.replace('{ts ', '').replace('}', '').replace(',N\'', ',\'').replace('*', '').replace('\ufeff', '').replace(';', '')
