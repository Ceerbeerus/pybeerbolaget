from datetime import date, timedelta
import urllib.parse
import json
import requests

async def get_beverage(api_key, type):
    SellStartDateFrom = date.today() - timedelta(days=31)
    SellStartDateTo = date.today() + timedelta(days=31)

    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'content-type': 'application/json'
    }

    url = 'api-extern.systembolaget.se/product/v1/product/search?'
    params = urllib.parse.urlencode({
        # Request parameters
        'SubCategory': type,
        'AssortmentText': 'Små partier',
        'SellStartDateFrom': SellStartDateFrom,
        'SellStartDateTo': SellStartDateTo,
    })
    all_beverages = []
    try:
        all_beverages = requests.get('https://api-extern.systembolaget.se/product/v1/product/search?%s' % params, headers=headers, verify=True).json()['Hits']
        all_beverages = sorted(all_beverages, key=lambda k: k['SellStartDate'])
    except:
        print ("Could not fetch data from api.")

    return all_beverages
