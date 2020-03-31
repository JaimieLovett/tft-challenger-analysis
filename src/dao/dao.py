import sqlite3
from sqlite3 import Error


class AppDAO:

    def __init__(self, db_file_path):
        self.con = None
        try:
            self.con = sqlite3.connect(db_file_path)
            self.cur = self.con.cursor()
        except Error as e:
            print(e)

    def run(self, sql, params=[]):
        try:
            self.cur.execute(sql, params)
            self.con.commit()
        except Error as e:
            print(e)

    def get(self, sql, params=[]):
        try:
            self.cur.execute(sql, params)
            rows = self.cur.fetchall()
            # self.con.commit()
            return rows
        except Error as e:
            print(e)
