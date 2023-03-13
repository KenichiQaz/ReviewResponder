'''   ~~~~~~   Google Review Responder   ~~~~~~   '''
import os
import pandas as pd
from google.cloud import language_v1 as lang
import requests

API_KEY = os.environ.get("GOOGLEAPIKEY")
PLACE_ID = ""  # the place id of the business
URL_START = "https://maps.googleapis.com/maps/api/place/details/json?"

def review_gatherer():
    ''' get reviews and pass them to the responder '''
    payload = {}
    headers = {}
    url = f'{URL_START}placeid={PLACE_ID}&fields=reviews&key={API_KEY}&reviews_sort=newest'
    json_response = requests.request(
        "GET", url, headers=headers, data=payload, timeout=5)
    business_reviews = json_response.json()
    for review in business_reviews['result']['reviews']:
        web_data = review
        print(review)
    if web_data != "":
        return web_data

def db_search():
    ''' Search the database '''
    database = pd.DataFrame()
    database = database.append(review_gatherer())
    database.to_csv('database.csv', mode='a', header=True)

db_search()