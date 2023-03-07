'''   ~~~~~~   Google Review Responder   ~~~~~~   '''
import os
import sqlite3
import pandas as pd
from google.cloud import language_v1 as lang
import requests

API_KEY = os.environ.get("GOOGLEAPIKEY")
PLACE_ID = "ChIJmQa2NZUrdTERWx3Ui77zN0c"  # ÆON MALL Tân Phú Celadon
URL_START = "https://maps.googleapis.com/maps/api/place/details/json?"


def connect_read_database():
    ''' Connect to the database '''
    conn = sqlite3.connect('reviews.db')
    cursor = conn.execute("SELECT * FROM Reviews")
    dataframe = pd.read_sql(cursor, conn)
    print("Operation done successfully")
    conn.close()
    return dataframe


def review_gather():
    ''' get reviews and pass them to the responder '''
    payload = {}
    headers = {}
    url = f'{URL_START}placeid={PLACE_ID}&fields=reviews&key={API_KEY}&reviews_sort=newest'
    print(url)
    json_response = requests.request(
        "GET", url, headers=headers, data=payload, timeout=5)
    business_reviews = json_response.json()
    for review in business_reviews['result']['reviews']:
        bus_data = pd.read_json(review)
    return bus_data


def review_responder(text):
    ''' take reviews and determine the sentiment, then respond appropriately '''
    client = lang.LanguageServiceClient()
    document = lang.Document(content=text, type_=lang.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(
        request={"document": document}).document_sentiment
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
    if os.path.exists("reviews.db"):
        database = pd.DataFrame()
        database = database.append(connect_read_database())
        database = database.append(review_gather())
    # get responder
    # Search the database for review id
    # write response if it is empty
