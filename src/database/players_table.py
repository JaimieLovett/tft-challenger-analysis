class PlayersTable():

    def __init__(self, dao):
        self.dao = dao

    def init(self):
        self.dao.run(
            """
            CREATE TABLE players (
            id integer PRIMARY KEY,
            name text NOT NULL,
            rank integer NOT NULL)
            """)

    def create(self, name, rank):
        self.dao.run(
            "INSERT INTO players (name, rank) VALUES (?, ?)",
            (name, rank))
