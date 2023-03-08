'''   ~~~~~~   Google Review Responder   ~~~~~~   '''
import os
import sqlite3
import pandas as pd
from google.cloud import language_v1 as lang
import requests

API_KEY = "AIzaSyB_w7goaSbR2tmHAllqpNLNKFmaqjfpSio" #os.environ.get("GOOGLEAPIKEY")
PLACE_ID = "ChIJmQa2NZUrdTERWx3Ui77zN0c"  # ÆON MALL Tân Phú Celadon
URL_START = "https://maps.googleapis.com/maps/api/place/details/json?"

def review_gatherer():
    ''' get reviews and pass them to the responder '''
    payload = {}
    headers = {}
    url = f'{URL_START}placeid={PLACE_ID}&fields=reviews&key={API_KEY}&reviews_sort=newest'
    print(url)
    json_response = requests.request("GET", url, headers=headers, data=payload, timeout=5)
    business_reviews = json_response.json()
    #print(business_reviews)
    # check if valid response is received
    for review in business_reviews['result']['reviews']:
        web_data = review
        print(review)
    #if webdata != "" then return webdata else return empty dataframe
    return web_data


def responder(text: str) -> str:
    ''' take reviews and determine the sentiment, then respond appropriately '''
    client = lang.LanguageServiceClient()
    document = lang.Document(content=text, type_=lang.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    # pylint: disable=C0301. # disable line too long error
    if sentiment.score < 0:
        response = "I'm sorry to hear that. Please tell us more about your experience so we can better our services."
    elif sentiment.score > 0:
        response = "Thank you for the kind words! We really appreciate your feedback."
    else:
        response = "We appreciate your feedback and we're always looking to improve our services."
    return response


def db_search():
    ''' Search the database '''
    database = pd.DataFrame()
    database = database.append(review_gatherer())
    database = database.reset_index()
    for row in database.iterrows():
        if row['Response'] == "":
            row['Response'] = responder(row['text'])
    

def test():
    database = review_gatherer()
    for row in database.iterrows():
            if row['Response'] == "":
                row['Response'] = responder(row['text'])
                print(row['Response'])
