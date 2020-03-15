from scrape.scraper import PlayerDataScraper
from database.dao import AppDAO
from database.regions_table import RegionsTable
from database.players_table import PlayersTable

dao = AppDAO('data/tft.db')

regions_table = RegionsTable(dao)
regions_table.init()
# regions_table.create('na')

players_table = PlayersTable(dao)
players_table.init()
#players_table.create('Test', 1)

scraper = PlayerDataScraper()
scraper.scrape()
