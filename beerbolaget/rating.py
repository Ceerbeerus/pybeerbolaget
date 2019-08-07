import re
import urllib.parse

import requests


class untappd_handle():
    def __init__(self, client_id, secret, token):
        self.client_id = client_id
        self.client_secret = secret
        self.token = token

    async def get_rating(self, brewery, name, detailed_name):
        have_had = None
        rating = None
        rating_by_user = None
        brewery = brewery.lower()
        name = name.lower()
        name_check = brewery.split(' ')
        if 'the' == name_check[0]:
            del name_check[0]
        brewery = name_check[0]
        if detailed_name:
            detailed_name = detailed_name.lower()
        beer_name = name
        if (detailed_name and name_check[0] in name and
                name_check[0] not in detailed_name):
            beer_name = detailed_name
        elif (detailed_name and name_check[0] not in name and
              name_check[0] not in detailed_name):
            beer_name += ' ' + detailed_name

        beer_name = re.sub(r'\d+', '', beer_name)
        beer_id = await self.get_beer_id(brewery, beer_name)
        if not beer_id and len(beer_name.split(' ')) > 1:
            beer_name = beer_name.split(' ')
            if (len(beer_name[0]) < 4 or brewery in beer_name[0]):
                if len(beer_name) > 2 and len(beer_name[1]) < 4:
                    beer_name = beer_name[2]
                else:
                    beer_name = beer_name[1]
            else:
                beer_name = beer_name[0]
            beer_id = await self.get_beer_id(brewery, beer_name)

        if beer_id:
            (rating,
             have_had,
             rating_by_user) = await self.get_beer_rating(beer_id)
            if rating:
                rating = round(rating, 2)
        return (rating, have_had, rating_by_user)

    async def get_beer_id(self, brewery, name):
        url = 'https://api.untappd.com/v4/search/beer?%s'
        params = urllib.parse.urlencode({
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'q': ' '.join([brewery, name])
        })
        resp = await self.make_request(url, params)

        best_match_id = None
        best_match_count = 0
        best_match_negativ_count = 100
        try:
            for beer in resp['beers']['items']:
                matches = ([x for x in name.split(' ') if
                            x in beer['beer']['beer_name'].lower()])

                neg_matches = ([x for x in beer['beer']['beer_name'].split()
                                if x.lower() not in name])

                if ((len(matches) > best_match_count or (len(matches) > 0 and
                     len(matches) == best_match_count and
                        len(neg_matches) < best_match_negativ_count)) and
                    (len(resp['beers']['items']) < 2 or
                        brewery in beer['brewery']['brewery_name'].lower())):

                    best_match_count = len(matches)
                    best_match_negativ_count = len(neg_matches)
                    best_match_id = beer['beer']['bid']

        except Exception as e:
            print("Could not read beer id from response: ({})".format(e))
        return best_match_id

    async def get_beer_rating(self, beer_id):
        url = ''.join(['https://api.untappd.com/v4/beer/info/',
                       str(beer_id), '?%s'])
        if self.token:
            params = urllib.parse.urlencode({
                'access_token': self.token,
                'compact': 'true'
            })
        else:
            params = urllib.parse.urlencode({
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'compact': 'true'
            })
        resp = await self.make_request(url, params)
        beer_rating = None
        have_had = None
        rating_by_user = None
        try:
            beer_rating = resp['beer']['rating_score']
            have_had = (resp['beer']['stats']['user_count'] > 0)
            rating_by_user = resp['beer']['auth_rating']
        except Exception as e:
            print("Could not read beer rating from response: ({})".format(e))
        return (beer_rating, have_had, rating_by_user)

    async def make_request(self, url, params):
        headers = {
            'content-type': 'application/json'
        }
        resp = []
        try:
            resp = requests.get(url % params, headers=headers,
                                verify=True).json()['response']
        except Exception as e:
            print("Could not fetch data from untappd api:  ({})".format(e))
        return resp
