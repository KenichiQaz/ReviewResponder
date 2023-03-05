import json
from datetime import datetime 
from google.cloud import language_v1
import types
import requests



# #Google Review Responder
gapi_Key = "AIzaSyB_w7goaSbR2tmHAllqpNLNKFmaqjfpSio"
place_id = "ChIJg5WqpxwodTERGZllG4JgTr0" #AEON Mall Binh Duong Canary
url_part1 = "https://maps.googleapis.com/maps/api/place/details/json?"

def review_gather():
    # Get all the google business reviews posted in the last hour 
    url = f'{url_part1}placeid={place_id}fields=reviews&key={gapi_Key}'
    response = requests.get(url, timeout=5)
    business_reviews = response.json()
    # # Loop through each review 
    for review in business_reviews['result']['reviews']:
    # # Get the time the review was posted in milliseconds
        review_time = review['time'] 
    # If the review was posted in the last hour 
        if review_time >= (datetime.time() * 1000) - 3600000:
        # # Do something with the review 
            # convert review to dataframe and then use to_csv to save results in the csv file.
            google_review_responder(review)

def google_review_responder(text): 
        # Instantiates a client
    client = language_v1.LanguageServiceClient()

    # The text to analyze
    text = "Hello, world!"
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    print("Text: {}".format(text))
    print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

# # Generate the response 
    if sentiment.score < 0: 
        response = "I'm sorry to hear that. We would love to hear more about your experience so that we can improve our services." 
    elif sentiment.score > 0: 
        response = "Thank you for the kind words! We really appreciate your feedback." 
    else: 
        response = "We appreciate your feedback and we're always looking to improve our services." 
    return response
