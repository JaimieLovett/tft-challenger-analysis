from scrape.scraper import TFTScraper
from database.dao import AppDAO
from database.players_table import PlayersTable

dao = AppDAO('data/tft.db')
players_table = PlayersTable(dao)
players_table.init()
players_table.create('Test', 1)

scraper = TFTScraper()
scraper.scrape()
