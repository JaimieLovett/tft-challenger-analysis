import pickle
import requests
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self, url_to_scrape):
        self.url = url_to_scrape
        self.regions = [
            'na',
            'br',
            'eune',
            'euw',
            'jp',
            'kr',
            'lan',
            'las',
            'oce',
            'tr',
            'ru'
        ]

        # A list for storing all of our cleaned data.
        self.data = list()

    def _get_html(self, url):
        '''
        Returns the HTML content for the provided URL
        '''
        page = requests.get(url)

        return BeautifulSoup(page.content, 'html.parser')


class MatchDataScraper(Scraper):

    def __init__(self, player):
        Scraper.__init__(self, 'https://lolchess.gg/profile/{0}/{1}')

        self.player = player

    def _get_url_to_scrape(self, site_url, region, player):
        '''
        A function to format the URL string we want to
        scrape by inserting the region and player name
        '''
        return site_url.format(region, player.replace(" ", ""))

    def _get_match_data(self, soup):
        match_history = []
        divs = soup.find_all(
            "div", {"class": "profile__match-history-v2__item"})
        for div in divs:
            match_placement = div.find("div", {"class": "placement"})
            match_mode = div.find("div", {"class": "game-mode"})
            match_length = div.find("div", {"class": "length"})
            traits = [trait.img['alt']
                      for trait in div.find_all(
                          "div", {"class": "tft-hexagon"})]
            units = [unit.img['alt']
                     for unit in div.find_all(
                         "div", {"class": "tft-champion"})]

            traits = pickle.dumps(traits)
            units = pickle.dumps(units)
            match_history.append(
                [
                    match_placement.text.replace("#", ""),
                    match_mode.text,
                    match_length.text,
                    traits,
                    units
                ]
            )
        return match_history

    def scrape(self):
        print('Scraping data for player "{0}" of {1} region...'.format(
            self.player[0], self.player[1].upper()))
        soup = self._get_html(
            self._get_url_to_scrape(
                self.url,
                self.player[1],
                self.player[0]))

        # Find the match history for player
        self.data = self._get_match_data(soup)

        print('Scraping Match data complete...')
        return self.data


class PlayerDataScraper(Scraper):

    def __init__(self):
        Scraper.__init__(
            self, 'https://lolchess.gg/leaderboards?region={0}&page={1}')

        # Work out how many pages we need to scrape.
        self.num_players = 200
        self.results_per_page = 100

    def _get_url_to_scrape(self, site_url, region, page_num):
        '''
        A function to format the URL string we want to
        scrape by inserting the region and page number
        '''
        return site_url.format(region, page_num)

    def _get_player_rows(self, soup):
        return soup.find_all('tr')

    def _get_cleaned_row(self, row):
        row = row.find_all('td')
        row = [z.text.strip() for z in row]
        row[1] = row[1][4:].strip()
        row[2] = row[2][:-2].strip()
        row[3] = row[3][:-5].strip()
        row[4] = row[4][:-1].strip()
        return row

    def scrape(self):
        print('Scraping Player data... Please wait...')

        num_regions_to_scrape = len(self.regions)
        num_pages_to_scrape = self.num_players // self.results_per_page

        for region in range(num_regions_to_scrape):

            print('Scraping {0} region...'.format(
                self.regions[region].upper()))

            for page in range(num_pages_to_scrape):
                soup = self._get_html(
                    self._get_url_to_scrape(
                        self.url,
                        self.regions[region], page + 1))

                # Find all rows on the page and delete the header row
                rows = self._get_player_rows(soup)
                del(rows[0])

                for row in rows:
                    clean_row = self._get_cleaned_row(row)
                    clean_row.append(self.regions[region])
                    self.data.append(clean_row)

        print('Scraping Player data complete...')
        return self.data
