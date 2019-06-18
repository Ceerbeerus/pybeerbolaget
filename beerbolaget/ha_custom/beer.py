from datetime import datetime
import json
from pybeerbolaget.ha_custom import common


class beer_handler():
    def __init__(self, api_key, ratebeer, untappd):
        self.api_key = api_key
        self.ratebeer = ratebeer
        self.untappd = untappd
        self.beers = []
        self.release = None

    async def update_new_beers(self):
        beer_available = await common.get_beverage(self.api_key, 'Öl')
        if len(beer_available) > 0:
            self.release = beer_available[-1]['SellStartDate']
        for beer_item in beer_available:
            if beer_item['SellStartDate'] == self.release:
                new_beer = beer(beer_item['Country'],
                                beer_item['Price'],
                                beer_item['ProducerName'],
                                beer_item['ProductNameBold'],
                                beer_item['ProductNameThin'],
                                beer_item['Type'])
                self.beers.append(new_beer)

    async def get_beers(self):
        beers = []
        for beer in self.beers:
            beers.append(beer.__dict__)
        return json.dumps(beers)

    async def get_release(self):
        return self.release.split('T')[0]


class beer():
    def __init__(self, brewery, name, detailed_name, type, price, country):
        self.brewery = brewery
        self.name = name
        self.detailed_name = detailed_name
        self.type = type
        self.price = price
        self.country = country
        self.rating = None
