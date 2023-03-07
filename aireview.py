'''   ~~~~~~   Google Review Responder   ~~~~~~   '''
import os
import time
import sqlite3
import pandas as pd
from google.cloud import language_v1 as lang
import requests

API_KEY = os.environ.get("GOOGLEAPIKEY")
PLACE_ID = "ChIJmQa2NZUrdTERWx3Ui77zN0c"  # ÆON MALL Tân Phú Celadon
URL_PART1 = "https://maps.googleapis.com/maps/api/place/details/json?"


def connect_read_database():
    ''' Connect to the database '''
    conn = sqlite3.connect('reviews.db')
    cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
    for row in cursor:
        dataframe = pd.DataFrame(row)
    print("Operation done successfully")
    conn.close()
    return dataframe


def review_gather():
    ''' get reviews and pass them to the responder '''
    payload = {}
    headers = {}
    # Get all the google business reviews posted in the last hour
    url = f'{URL_PART1}placeid={PLACE_ID}&fields=reviews&key={API_KEY}&reviews_sort=newest'
    print(url)
    json_response = requests.request(
        "GET", url, headers=headers, data=payload, timeout=5)
    business_reviews = json_response.json()

    for review in business_reviews['result']['reviews']:
        review_time = review['time']
        unix_timestamp = int(review_time)
        utc_time = time.gmtime(unix_timestamp)
        print(time.strftime("%Y-%m-%d %H:%M:%S+00:00 (UTC)", utc_time))
        return review_responder(review)
#   add response to database


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
    # Search the database for review id
    # write response if it is empty
    return "pass"
