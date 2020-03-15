from scrape.scraper import PlayerDataScraper
from scrape.scraper import MatchDataScraper
from database.dao import AppDAO
from database.players_table import PlayersTable

dao = AppDAO('data/tft.db')

players_table = PlayersTable(dao)
players_table.init()

player_scraper = PlayerDataScraper()
players = player_scraper.scrape()

for player in players:
    players_table.create(*player)

for player in players_table.getAllNamesAndRegions():
    match_scraper = MatchDataScraper(player)
    player_match_history = match_scraper.scrape()
