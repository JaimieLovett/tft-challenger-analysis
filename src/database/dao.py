import sqlite3
from sqlite3 import Error


class AppDAO:

    def __init__(self, db_file_path):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file_path)
            print(sqlite3.version)
        except Error as e:
            print(e)
