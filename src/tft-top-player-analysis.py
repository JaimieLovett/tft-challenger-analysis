from scrape.scraper import PlayerDataScraper
from scrape.scraper import MatchDataScraper
from dao.dao import AppDAO
from dao.players_table import PlayersTable
from dao.matches_table import MatchesTable


def database_setup():
    '''
    Create the TFT database, as well as the players
    and matches tables.
    '''
    dao = AppDAO('data/raw/tft.db')

    players_table = PlayersTable(dao)
    players_table.init()

    matches_table = MatchesTable(dao)
    matches_table.init()

    return players_table, matches_table


def scrape_players():
    player_scraper = PlayerDataScraper()
    players = player_scraper.scrape()

    return players


def scrape_match_history(player):
    match_scraper = MatchDataScraper(player[0])
    player_match_history = match_scraper.scrape()

    return player_match_history


def populate_players_table(players, players_table):
    for player in players:
        players_table.create(*player)


def main():  
    NUM_SCRAPE_ITERATIONS = 50
    
    players_table, matches_table = database_setup()
    players = scrape_players()
    populate_players_table(players)

    # Scrape multiple times to make sure we collect as much data as possible
    for i in range(NUM_SCRAPE_ITERATIONS):
        # Get all of the id's of the players that have scraped match history data
        scraped_ids = matches_table.getAllPlayerIds()
        # Get all of the id's for players in the players_table
        player_ids = players_table.getAllIds()
        # Calculate which players are in the players_table but we have no match history data for
        ids_to_scrape = list(set(player_ids) - set(scraped_ids))

        for id in ids_to_scrape:
            # Get the name and region for each player so we can scrape their data
            player = players_table.getNameAndRegionById(id[0])
            # Scrape the match history for each player
            player_match_history = scrape_match_history(player)
            # Populate the matches_table
            for match in player_match_history:
                matches_table.create(id[0], *match)


if __name__ == "__main__":
    main()
