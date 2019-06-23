from datetime import date, timedelta
import urllib.parse

import requests


async def get_latest_release(api_key, type='Öl'):
    SellStartDateFrom = date.today() - timedelta(days=31)
    SellStartDateTo = date.today() + timedelta(days=31)

    latest = None
    params = urllib.parse.urlencode({
        # Request parameters
        'SubCategory': type,
        'AssortmentText': 'Små partier',
        'SellStartDateFrom': SellStartDateFrom,
        'SellStartDateTo': SellStartDateTo,
    })
    beverages = await make_request(api_key, params)
    if len(beverages) > 0:
        latest = beverages[-1]['SellStartDate']
    return latest


async def get_beverage(api_key, release_date, type='Öl'):
    params = urllib.parse.urlencode({
        # Request parameters
        'SubCategory': type,
        'AssortmentText': 'Små partier',
        'SellStartDateFrom': release_date,
        'SellStartDateTo': release_date,
    })
    beverages = await make_request(api_key, params)
    return beverages


async def make_request(api_key, params):
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'content-type': 'application/json'
    }

    all_beverages = []
    try:
        all_beverages = requests.get(
            'https://api-extern.systembolaget.se/product/v1/product/search?%s' % params,
            headers=headers, verify=True).json()['Hits']
        all_beverages = sorted(all_beverages, key=lambda k: k['SellStartDate'])
    except Exception as e:
        print("Could not fetch data from api ({})".format(e))

    return all_beverages
