'''   ~~~~~~   Google Review Responder   ~~~~~~   '''
import os
import time
import datetime
from google.cloud import language_v1 as lang
import requests
import pandas as pd
import json
from pandas import json_normalize

API_KEY = os.environ.get("GOOGLEAPIKEY")
PLACE_ID = "ChIJmQa2NZUrdTERWx3Ui77zN0c"  # ÆON MALL Tân Phú Celadon
URL_PART1 = "https://maps.googleapis.com/maps/api/place/details/json?"


def review_gather():
    '''get reviews and pass them to the responder'''

    # Get all the google business reviews posted in the last hour
    url = f'{URL_PART1}placeid={PLACE_ID}&fields=reviews&key={API_KEY}&reviews_sort=newest'
    print(url)
    payload = {}
    headers = {}

    response = requests.request(
        "GET", url, headers=headers, data=payload, timeout=5)
    business_reviews = response.json()
    # # Loop through each review
    df = pd.json_normalize(business_reviews['result']['reviews'])

    for review in business_reviews['result']['reviews']:
        # # Get the time the review was posted in milliseconds
        responsestr = ""
        review_time = review['time']
        unix_timestamp  = int(review_time)
        utc_time = time.gmtime(unix_timestamp)
        print(time.strftime("%Y-%m-%d %H:%M:%S+00:00 (UTC)", utc_time))  
    # If the review was posted in the last hour
        responsestr = review_responder(review)
        df['response'] = responsestr
    if os.path.exists("reviews.csv"):
        df.to_csv("reviews.csv", mode='a', index=True, header=False)
    else:
        df.to_csv("reviews.csv", mode='w', index=True, header=True)


def review_responder(text):
    '''take reviews and determine the sentiment, then respond appropriately'''

    # Instantiates a client
    client = lang.LanguageServiceClient()

    # The text to analyze
    text = "Hello, world!"
    document = lang.Document(
        content=text, type_=lang.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    print(f"Text: {text}")
    print(f"Sentiment: {sentiment.score}, {sentiment.magnitude}")

# # Generate the response
    if sentiment.score < 0:
        response = "I'm sorry to hear that. We would love to hear more about your experience so that we can improve our services."
    elif sentiment.score > 0:
        response = "Thank you for the kind words! We really appreciate your feedback."
    else:
        response = "We appreciate your feedback and we're always looking to improve our services."
    return response


review_gather()
