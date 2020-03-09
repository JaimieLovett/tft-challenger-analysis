import os
import csv
import requests
from bs4 import BeautifulSoup

# The URL to scrape and all of the regions we're interested in
url_to_scrape = 'https://lolchess.gg/leaderboards?region={0}&page={1}'
regions_to_scrape = ['na', 'br', 'eune', 'euw',
                     'jp', 'kr', 'lan', 'las', 'oce', 'tr', 'ru']

# Work out how many pages we need to scrape to get the num of results we want
num_results_to_scrape = 500
results_per_page = 100
num_pages_to_scrape = num_results_to_scrape // results_per_page

# A list for storing all of our cleaned data before we write it to CSV
tft_cleaned_data_list = []
output_file_path = os.path.abspath(
    __file__) + '\\..\\..\\data\\tft-summoner-stats.csv'
csv_head = ['rank', 'name', 'tier', 'lp',
            'win rate', 'played', 'wins', 'losses', 'region']


def get_url_to_scrape(region, page_num):
    '''
    A function to format the URL string we want to scrape by inserting
    the region and page number
    '''
    return requests.get(url_to_scrape.format(region, page_num))


# Scrape data for each region, on each page
for x in range(len(regions_to_scrape)):
    for y in range(num_pages_to_scrape):
        soup = BeautifulSoup(get_url_to_scrape(
            regions_to_scrape[x], y + 1).content, 'html.parser')

        # Find all rows on the page and delete the first row of headings
        rows = soup.find_all('tr')
        del (rows[0])

        # Clean each row of data
        for row in rows:
            row = row.find_all('td')
            row = [z.text.strip() for z in row]
            row[1] = row[1][4:].strip()
            row[2] = row[2][:-2].strip()
            row[3] = row[3][:-5].strip()
            row[4] = row[4][:-1].strip()
            row.append(regions_to_scrape[x])
            tft_cleaned_data_list.append(row)

# Write our cleaned data to a CSV file
with open(output_file_path, 'a', encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_head)
    for row in tft_cleaned_data_list:
        writer.writerow(row)
