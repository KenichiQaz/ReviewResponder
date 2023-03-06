'''   ~~~~~~   Google Review Responder   ~~~~~~   '''
import datetime
from google.cloud import language_v1 as lang
import requests
import os

'''  API Key will be moved to environment soon also testing the autocommit '''
API_KEY = os.environ.get("GOOGLEAPIKEY")
PLACE_ID = "ChIJg5WqpxwodTERGZllG4JgTr0"  # AEON Mall Binh Duong Canary
URL_PART1 = "https://maps.googleapis.com/maps/api/place/details/json?"


def review_gather():
    '''get reviews and pass them to the responder'''

    # Get all the google business reviews posted in the last hour
    url = f'{URL_PART1}placeid={PLACE_ID}fields=reviews&key={API_KEY}'
    print(url)
    response = requests.get(url, timeout=5)
    business_reviews = response.json()
    # # Loop through each review
    for review in business_reviews['result']['reviews']:
        # # Get the time the review was posted in milliseconds
        review_time = review['time']
    # If the review was posted in the last hour
        if review_time >= (datetime.time() * 1000) - 3600000:
            # convert review to dataframe and then use to_csv to save results in the csv file.
            review_responder(review)


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