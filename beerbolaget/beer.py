﻿import json
from beerbolaget import common, rating


class beer_handler():
    def __init__(self, api_key, image_url, ratebeer, store,
                 untappd_client, untappd_secret, untappd_token):
        self.api_key = api_key
        self.beers = {}
        self.chosen_store = store
        self.image_url = image_url
        self.ratebeer = ratebeer
        self.release = None
        self.store_name = None
        self.store_id = None
        self.untappd_handle = rating.untappd_handle(untappd_client,
                                                    untappd_secret,
                                                    untappd_token)

    def get_store_info(self):
        if self.chosen_store:
            (self.store_id,
             self.store_name) = common.get_store_info(self.api_key,
                                                      self.chosen_store)

    def update_new_beers(self):
        self.release = common.get_latest_release(self.api_key)

        if self.release:
            beer_available = common.get_beverage(self.api_key,
                                                 self.release)
            # Clear previous beer list
            self.beers.clear()

            for item in beer_available:
                available_in_store = False
                if (self.store_id and
                        self.store_id in item['IsInStoreSearchAssortment']):
                    available_in_store = True
                new_beer = beer(available_in_store,
                                item['ProducerName'],
                                item['ProductNumber'],
                                item['ProductNameBold'],
                                item['ProductNameThin'],
                                item['Type'],
                                item['Price'],
                                item['Country'],
                                item['SellStartDate'],
                                show_availability=(self.store_id is not None))
                self.beers[item['ProductId']] = new_beer

    def get_images(self):
        if self.image_url and len(self.beers) > 0:
            images = common.get_images(self.release, self.image_url)
            for beer in self.beers:
                if beer in images:
                    self.beers[beer].image = images[beer]['ImageUrl']

    def get_ratings(self):
        if self.untappd_handle.client_id and len(self.beers) > 0:
            for beer in self.beers:
                brewery = self.beers[beer].brewery
                name = self.beers[beer].name
                detailed_name = self.beers[beer].detailed_name
                (self.beers[beer].untappd_rating,
                 self.beers[beer].untappd_checked_in,
                 self.beers[beer].untappd_rating_by_user) = (
                    self.untappd_handle.get_rating(brewery,
                                                   name,
                                                   detailed_name))

    def get_beers(self):
        beers = []
        for beer in self.beers:
            beers.append(self.beers[beer].__dict__)
        if len(beers) > 0:
            beers = sorted(beers, key=lambda k: k['id'])
        return beers

    def get_release(self):
        if self.release:
            return self.release.split('T')[0]
        else:
            return "No release could be found."

    def get_store(self):
        return self.store_name


class beer():
    def __init__(self, availability_local, brewery, id, name, detailed_name,
                 type, price, country, release, show_availability=False):
        self.availability_local = availability_local
        self.brewery = brewery
        self.country = country
        self.detailed_name = detailed_name
        self.id = id
        self.image = None
        self.name = name
        self.price = price
        self.release_date = release
        self.untappd_checked_in = None
        self.untappd_rating = None
        self.untappd_rating_by_user = None
        self.show_availability = show_availability
        self.type = type
