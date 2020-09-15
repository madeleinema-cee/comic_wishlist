import pdb
import sys
import sqlite3
import os
import time


class Db:
    def __init__(self, database, db_file=None):
        self.conn = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.db_file = db_file

        self.create = False
        self.insert = False
        self.current_query = []

        self.insert_data_to_be_replaced = [('{ts', ''), ('}', ''), (',N\'', ',\''), ('*', '')]

        if self.db_file:
            # os.remove('comic_wishlist.db')
            self.conn = sqlite3.connect(database, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.parse_database_file()

    def execute(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def parse_database_file(self):
        with open(self.db_file, encoding='utf-16') as f:
            table_mode = True
            for index, line in enumerate(f):
                if index % 1000 == 0:
                    print(index)

                if 'INSERT INTO' in line:
                    table_mode = False

                # if table_mode:
                #     self.create_table(line)
                if table_mode is False:
                    self.insert_data(line)

    def create_table(self, line):
        if 'GO' in line:
            query = ''.join(self.current_query)
            self.execute(query)
            self.create = False

        if 'CREATE TABLE' in line:
            self.create = True
            self.current_query = []

        if self.create:
            self.current_query.append(line.strip())

    def insert_data(self, line):
        if 'GO' in line:

            query = ''.join(self.current_query).strip()
            for rep in self.insert_data_to_be_replaced:
                query = query.replace(rep[0], rep[1])

            try:
                self.execute(query)
            except Exception as e:
                print(f'{e}\n{query}\n\n')

            self.insert = False

        if 'INSERT INTO' in line and '[Issue]' in line:
            self.insert = True
            self.current_query = []

        if self.insert:
            self.current_query.append(line.strip())


if __name__ == '__main__':
    start = time.time()
    db = Db('comic_wishlist.db', 'data.sql')
    end = time.time()
    print(end - start)
