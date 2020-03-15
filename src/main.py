from scrape.scraper import PlayerDataScraper
from database.dao import AppDAO
from database.players_table import PlayersTable

dao = AppDAO('data/tft.db')

players_table = PlayersTable(dao)
players_table.init()

scraper = PlayerDataScraper()
players = scraper.scrape()

for player in players:
    players_table.create(*player)
