import json
from beerbolaget.ha_custom import common


class beer_handler():
    def __init__(self, api_key, image_url, ratebeer, store, untappd):
        self.api_key = api_key
        self.beers = {}
        self.image_url = image_url
        self.ratebeer = ratebeer
        self.release = None
        self.store_name = store
        self.store_id = None
        self.untappd = untappd

    async def get_store_info(self):
        if self.store_name:
            self.store_id = await common.get_store_id(self.api_key,
                                                      self.store_name)

    async def update_new_beers(self):
        self.release = await common.get_latest_release(self.api_key)

        if self.release:
            beer_available = await common.get_beverage(self.api_key,
                                                       self.release)
            for item in beer_available:
                available_in_store = False
                if (self.store_id and
                        self.store_id in item['IsInStoreSearchAssortment']):
                    available_in_store = True
                new_beer = beer(available_in_store,
                                item['ProducerName'],
                                item['ProductNameBold'],
                                item['ProductNameThin'],
                                item['Type'],
                                item['Price'],
                                item['Country'],
                                show_availability=(self.store_id is not None))
                self.beers[item['ProductId']] = new_beer

    async def get_images(self):
        if self.image_url and len(self.beers) > 0:
            images = await common.get_images(self.release, self.image_url)
            for beer in self.beers:
                if beer in images:
                    self.beers[beer].image = images[beer]['ImageUrl']

    async def get_beers(self):
        beers = []
        for beer in self.beers:
            beers.append(self.beers[beer].__dict__)
        return json.dumps(beers, ensure_ascii=False)

    async def get_release(self):
        return self.release.split('T')[0]


class beer():
    def __init__(self, availability_local, brewery, name, detailed_name,
                 type, price, country, show_availability=False):
        self.availability_local = availability_local
        self.brewery = brewery
        self.country = country
        self.detailed_name = detailed_name
        self.image = None
        self.name = name
        self.price = price
        self.rating = None
        self.show_availability = show_availability
        self.type = type
