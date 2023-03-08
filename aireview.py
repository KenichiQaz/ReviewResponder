'''   ~~~~~~   Google Review Responder   ~~~~~~   '''
import os
import sqlite3
import pandas as pd
from google.cloud import language_v1 as lang
import requests


API_KEY = os.environ.get("GOOGLEAPIKEY")
PLACE_ID = "ChIJmQa2NZUrdTERWx3Ui77zN0c"  # ÆON MALL Tân Phú Celadon
URL_START = "https://maps.googleapis.com/maps/api/place/details/json?"

def gmaps_get_reviews():
    gmaps = googlemaps.Client(key=API_KEY)
    place = gmaps.place('ChIJmxoAhvdX4joR9aZdwt5FjgE')
    place['result']['reviews']

def connect_read_database():
    ''' Connect to the database '''
    conn = sqlite3.connect('reviews.db')
    cursor = conn.execute("SELECT * FROM Reviews")
    database_data = pd.read_sql(cursor, conn)
    print("Operation done successfully")
    conn.close()
    return database_data


def review_gatherer():
    ''' get reviews and pass them to the responder '''
    payload = {}
    headers = {}
    url = f'{URL_START}placeid={PLACE_ID}&fields=reviews&key={API_KEY}&reviews_sort=newest'
#    print(url)
    json_response = requests.request(
        "GET", url, headers=headers, data=payload, timeout=5)
    business_reviews = json_response.json()
    # check if valid response is received
    for review in business_reviews['result']['reviews']:
        web_data = pd.read_json(review)
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
    if os.path.exists("reviews.db"):
        database = database.append(connect_read_database())
        database = database.append(review_gatherer())
        database = database.reset_index()
        for row in database.iterrows():
            if row['Response'] == "":
                row['Response'] = responder(row['text'])
        conn = sqlite3.connect('reviews.db')
        database.to_sql('Reviews', conn, if_exists='replace', index = False)
        conn.close()
    # get responder
    # Search the database for review id
    # write response if it is empty
