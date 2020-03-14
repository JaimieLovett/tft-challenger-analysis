class PlayersTable():

    def __init__(self, dao):
        self.dao = dao

    def init(self):
        self.dao.run(
            """
            CREATE TABLE players (
            id integer PRIMARY KEY AUTOINCREMENT,
            rank integer NOT NULL,
            name text NOT NULL UNIQUE)
            """)

    def create(self, name, rank):
        self.dao.run(
            "INSERT INTO players (name, rank) VALUES (?, ?)",
            [name, rank])
