from db import Db
import os
import argparse
import pdb

class SQLFileParser:
    def __init__(self, sql_path):
        db_path = 'comic_wishlist.db'
        if os.path.isfile(db_path):
            os.remove(db_path)
        self.db = Db(db_path)
        self.database = 'comics'
        self.sql_path = sql_path
        self.intermediary_file = '/tmp/int.txt'
        self.unwanted_lines = ['--']
        self.queries = []

    def main(self):
        with open(self.sql_path, encoding='utf-16') as f, open(self.intermediary_file, 'w+') as i:
            for idx, line in enumerate(f):
                if line[0:2] not in self.unwanted_lines:
                    try:
                        i.write(line.strip('\r\n'))
                    except Exception as e:
                        pdb.set_trace()
                        print(e)
                        print(line)
                        print(idx)

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str)
    args = parser.parse_args()
    s = SQLFileParser(args.file_path)
    s.main()
