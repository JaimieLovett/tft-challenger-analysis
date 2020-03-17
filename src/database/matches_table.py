class MatchesTable():

    def __init__(self, dao):
        self.dao = dao

    def init(self):
        self.dao.run(
            """
            CREATE TABLE matches (
            matchid     INTEGER     PRIMARY KEY     AUTOINCREMENT,
            playerid    INTEGER     NOT NULL,
            placement   INTEGER     NOT NULL,
            mode        TEXT        NOT NULL,
            length      TEXT        NOT NULL,
            traits      TEXT        NOT NULL,
            units       TEXT        NOT NULL)
            """)

    def create(self, playerid, placement, mode, length, traits, units):
        return self.dao.run(
            '''
            INSERT OR IGNORE INTO matches
            (playerid, placement, mode, length, traits, units)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            [playerid, placement, mode, length, traits, units])

    def getAllPlayerIds(self):
        return self.dao.get(
            '''
            SELECT playerid FROM matches
            '''
        )
