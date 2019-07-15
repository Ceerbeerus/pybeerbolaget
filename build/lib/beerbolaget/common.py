from datetime import date, timedelta
import urllib.parse

import requests


async def get_beverage(api_key, release_date, type='Öl'):
    url = 'https://api-extern.systembolaget.se/product/v1/product/search?%s'
    params = urllib.parse.urlencode({
        # Request parameters
        'SubCategory': type,
        'AssortmentText': 'Små partier',
        'SellStartDateFrom': release_date,
        'SellStartDateTo': release_date,
    })
    beverages = await make_request(api_key, url, params)
    return beverages


async def get_images(release_date, image_url, type='Öl'):
    url = image_url + '/?%s'
    headers = {
        'content-type': 'application/json'
    }
    params = urllib.parse.urlencode({
        # Request parameters
        'SubCategory': type,
        'AssortmentText': 'Små partier',
        'SellStartDateFrom': release_date,
        'SellStartDateTo': release_date,
    })
    images = []
    try:
        images = requests.get(
            url % params,
            headers=headers, verify=True).json()['ProductSearchResults']
    except Exception as e:
        print("Could not fetch images:  ({})".format(e))

    image_urls = {}
    if len(images) > 0:
        for i in images:
            image_urls[i['ProductId']] = i['Thumbnail']
    return image_urls


async def get_latest_release(api_key, type='Öl'):
    SellStartDateFrom = date.today() - timedelta(days=31)
    SellStartDateTo = date.today() + timedelta(days=31)

    latest = None
    url = 'https://api-extern.systembolaget.se/product/v1/product/search?%s'
    params = urllib.parse.urlencode({
        # Request parameters
        'SubCategory': type,
        'AssortmentText': 'Små partier',
        'SellStartDateFrom': SellStartDateFrom,
        'SellStartDateTo': SellStartDateTo,
    })
    beverages = await make_request(api_key, url, params)
    if len(beverages) > 0:
        beverages = sorted(beverages, key=lambda k: k['SellStartDate'])
        latest = beverages[-1]['SellStartDate']
    return latest


async def get_store_info(api_key, chosen_store):
    store_id = None
    store_name = None
    url = 'https://api-extern.systembolaget.se/site/v1/site/search?%s'
    params = urllib.parse.urlencode({
        # Request parameters
        'SearchQuery': chosen_store
    })
    store = await make_request(api_key, url, params)
    if len(store) > 0:
        for s in store:
            if chosen_store.lower() in s['DisplayName'].lower():
                store_id = s['SiteId']
                store_name = s['Name']
    return (store_id, store_name)


async def make_request(api_key, url, params):
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'content-type': 'application/json'
    }

    resp = []
    try:
        resp = requests.get(
            url % params,
            headers=headers, verify=True).json()['Hits']
    except Exception as e:
        print("Could not fetch data from api:  ({})".format(e))

    return resp
