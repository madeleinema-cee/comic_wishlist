import sqlite3
import os
import time
import sys
import pprint

pp = pprint.PrettyPrinter(indent=2)\


class Db:
    def __init__(self, database, db_file=None):
        self.conn = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.db_file = db_file

        self.create = False
        self.insert = False

        self.current_query = []
        self.vals = []
        self.table = None

        self.current_table = None

        self.insert_data_to_be_replaced = [('{ts ', ''), ('}', ''), (',N\'', ',\''), ('*', '')]

        if self.db_file:
            os.remove('comic.db')
            self.conn = sqlite3.connect(database, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.parse_database_file()

    def execute(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def executemany(self, stmt, vals):
        self.cursor.executemany(stmt, vals)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def parse_database_file(self):
        with open(self.db_file, encoding='utf-16') as f:
            table_mode = True
            for index, line in enumerate(f):
                if index % 1000 == 0:
                    print(index)

                if table_mode is False:
                    if 'INSERT INTO' in line:
                        if self.current_table is None or self.current_table != self.get_current_table(line):
                            self.current_table = self.get_current_table(line)

                        cols = self.get_column_count(line)

                        print(self.current_table)
                        print(line)
                        sys.exit(1)

                if 'INSERT INTO' in line:
                    table_mode = False

                if table_mode:
                    self.create_table(line)

    def create_table(self, line):
        if 'GO' in line:
            query = ''.join(self.current_query)
            # print(query)
            self.execute(query)
            self.create = False

        if 'CREATE TABLE' in line:
            self.create = True
            self.current_query = []

        if self.create:
            self.current_query.append(line.strip())

    def get_current_table(self, line):
        return line[line.find('[')+1:line.find(']')]

    def get_col_count(self, line):

if __name__ == '__main__':
    start = time.time()
    db = Db('comic.db', 'data.sql')
    end = time.time()
    print(end - start)