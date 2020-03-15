class PlayersTable():

    def __init__(self, dao):
        self.dao = dao

    def init(self):
        self.dao.run(
            """
            CREATE TABLE players (
            playerid    INTEGER     PRIMARY KEY     AUTOINCREMENT,
            rank        INTEGER     NOT NULL,
            name        TEXT        NOT NULL,
            tier        TEXT        NOT NULL,
            lp          INTEGER     NOT NULL,
            winrate     REAL        NOT NULL,
            played      INTEGER     NOT NULL,
            wins        INTEGER     NOT NULL,
            losses      INTEGER     NOT NULL,
            region      TEXT        NOT NULL,
            UNIQUE(name, region))
            """)

    def create(self, rank, name, tier, lp,
               winrate, played, wins, losses, region):
        return self.dao.run(
            '''
            INSERT OR IGNORE INTO players
            (rank, name, tier, lp, winrate, played, wins, losses, region)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            [rank, name, tier, lp, winrate, played, wins, losses, region])

    def getAll(self):
        return self.dao.get(
            '''
            SELECT * FROM players
            '''
        )

    def getAllNames(self):
        return self.dao.get(
            '''
            SELECT name FROM players
            '''
        )

    def getAllNamesAndRegions(self):
        return self.dao.get(
            '''
            SELECT name, region FROM players LIMIT 5
            '''
        )
