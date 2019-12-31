import requests
from bs4 import BeautifulSoup
import json
import csv
import time

class WebScraper():
    def __init__(self, pages):
        self.pages = pages

    results = []
    baseUrl = 'https://www.otodom.pl/wynajem/mieszkanie/?page='
    def fetch(self, url):
        responese = requests.get(url)
        return responese

    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        content.encode('ascii', 'replace')
        locations = [location.text for location in content.findAll('p', {'class':'text-nowrap'})]
        rooms = [room.text for room in content.findAll('li', {'class':'offer-item-rooms'})]
        prices = [price.text.strip() for price in content.findAll('li', {'class':'offer-item-price'})]
        prices = [item.replace(" ", "") for item in prices]
        areas = [area.text.strip() for area in content.findAll('li', {'class':'offer-item-area'})]
        print(areas)
        for index in range(0, len(locations)):
            self.results.append({
                'location': locations[index],
                'rooms': rooms[index],
                'price': prices[index],
                'area': areas[index]
            })

    def to_csv(self):
        with open('all_offers.csv', 'w', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)


    def run(self):
        for page in range(1, self.pages):
            next_page = self.baseUrl + str(page)
            response = self.fetch(next_page)
            if response.status_code == 200:
                self.parse(response.text)
            else:
                print("Coś poszło nie tak.")
                continue
            time.sleep(2)
        self.to_csv()

if __name__ == '__main__':
    scrapper = WebScraper()
    scrapper.run()
