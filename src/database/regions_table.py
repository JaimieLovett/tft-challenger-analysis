class RegionsTable():

    def __init__(self, dao):
        self.dao = dao

    def init(self):
        self.dao.run(
            """
            CREATE TABLE regions (
            id integer PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL UNIQUE)
            """)

    def create(self, name):
        self.dao.run(
            "INSERT INTO regions (name) VALUES (?)",
            [name])
