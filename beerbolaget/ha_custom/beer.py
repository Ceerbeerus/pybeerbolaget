from datetime import datetime
import json
from beerbolaget.ha_custom import common


class beer_handler():
    def __init__(self, api_key, ratebeer, untappd):
        self.api_key = api_key
        self.ratebeer = ratebeer
        self.untappd = untappd
        self.beers = {}
        self.release = None

    async def update_new_beers(self):
        self.release = await common.get_latest_release(self.api_key)

        if self.release:
            beer_available = await common.get_beverage(self.api_key, self.release)
            for beer_item in beer_available:
                new_beer = beer(beer_item['ProducerName'],
                                beer_item['ProductNameBold'],
                                beer_item['ProductNameThin'],
                                beer_item['Type'],
                                beer_item['Price'],
                                beer_item['Country'])
                self.beers[beer_item['ProductId']] = new_beer

    async def get_beers(self):
        beers = []
        for beer in self.beers:
            beers.append(self.beers[beer].__dict__)
        return json.dumps(beers, ensure_ascii=False)

    async def get_release(self):
        return self.release.split('T')[0]


class beer():
    def __init__(self, brewery, name, detailed_name, type, price, country, show_availability=False):
        self.availability_local = 0
        self.availability_web = 0
        self.brewery = brewery
        self.name = name
        self.detailed_name = detailed_name
        self.type = type
        self.price = price
        self.country = country
        self.rating = None
        self.show_availability = show_availability
