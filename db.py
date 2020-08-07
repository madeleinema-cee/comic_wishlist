import sqlite3
import os
import time
import pprint

pp = pprint.PrettyPrinter(indent=2)
import pdb

import pandas as pd

class Db:
    def __init__(self, database, db_file=None):
        self.conn = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.conn.row_factory = sqlite3.Row
        self.db_file = db_file

        self.create = False
        self.insert = False
        self.current_query = []
        self.vals = []
        self.table = None
        self.data = None

        self.insert_data_to_be_replaced = [('{ts ', ''), ('}', ''), (',N\'', ',\''), ('*', '')]

        # if self.db_file:
        #     os.remove(database)
        #     self.conn = sqlite3.connect(database, check_same_thread=False)
        #     # with open(self.db_file, 'r', encoding='utf-16') as f:
        #
        #         # self.conn.executescript(f.read().replace('GO', '').replace('{ts ', '').replace('INSERT INTO', '').replace(';', '').\
        #         #     replace('}', '').replace(',N\'', ',\'').replace('*', ''))
        #         # self.conn.commit()
        #     self.cursor = self.conn.cursor()
        #     # self.parse_database_file()
        #     # self.insert_query()

    def execute(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def executemany(self, stmt, vals):
        self.cursor.executemany(stmt, vals)
        self.conn.commit()

    def fetchall(self, query):
        self.cursor = self.conn.cursor()
        self.execute(query)
        result = [dict(row) for row in self.cursor.fetchall()]
        return result

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

                if table_mode is False:
                    tables = ['[User]']
                    for table in tables:
                        if table in line:
                            self.table = table
                            self.insert_data(line)


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


    def insert_data(self, line):
        self.insert = True
        self.current_query = []

        if self.insert:
            if self.table in line and 'INSERT INTO' in line:
                self.current_query.append(line.strip())
                query = ''.join(self.current_query).strip()

                self.data = query.replace('{ts ', '').replace('INSERT INTO', '').replace(';', '').\
                    replace('}', '').replace(',N\'', ',\'').replace('*', '')
                value = self.data.partition('VALUES')[2]
                # print(value)
                values = tuple(
                    value.replace('(', '').replace(')', '').replace('\'', '').replace(';', '').strip().split(',', 18))

                # if len(values) < 6:
                    # pdb.set_trace()
                    # print(values)
                self.vals.append(values)

                self.insert = False


    def insert_query(self):

        columns = self.data.partition('VALUES')[0]
        column = columns.partition('(')[2]
        item = column.count('[')
        value = ', ?' * (item - 1)
        values = '?' + value
        for idx, val in enumerate(self.vals):
            if len(val) != item:
                print(val)
                print(len(val))
                print(idx)
        # print(self.vals)
        try:
            stmt = f'INSERT INTO {columns} VALUES ({values})'

        # # print(stmt)


            # pp.pprint(self.vals)
            # Some values have more than the statement bindings supplied. See scratch_2.txt
            self.executemany(stmt, self.vals)
            # print(self.vals)
            # print(stmt)

        except Exception as e:
            print(f'{e}\n{self.data}\n\n')

        self.insert = False




if __name__ == '__main__':
    start = time.time()
    db = Db('comic_wishlist.db', 'data.sql')
    end = time.time()
    print(end - start)





