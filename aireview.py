import json
from datetime import datetime 
from google.cloud import requests 
from google.cloud.language import language, enums
import types
# #Google Review Responder
gapi_Key = "AIzaSyB_w7goaSbR2tmHAllqpNLNKFmaqjfpSio"
place_id = "ChIJg5WqpxwodTERGZllG4JgTr0" #AEON Mall Binh Duong Canary
url_part1 = "https://maps.googleapis.com/maps/api/place/details/json?"

def review_gather():
    # Get all the google business reviews posted in the last hour 
    url = f'{url_part1}placeid={place_id}fields=reviews&key={gapi_Key}'
    response = requests.get(url)
    business_reviews = response.json()
    # # Loop through each review 
    for review in business_reviews['result']['reviews']:
    # # Get the time the review was posted in milliseconds
        review_time = review['time'] 
    # If the review was posted in the last hour 
    if review_time >= (datetime.time() * 1000) - 3600000:
    # # Do something with the review 
        # convert review to dataframe and then use to_csv to save results in the csv file.
        print(review) 

def google_review_responder(text): 
# nitialize the Google Natural Language API 
    client = language.LanguageServiceClient() 
# # Analyze the sentiment of the text 
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT) 
    sentiment = client.analyze_sentiment(document=document).document_sentiment 
# # Generate the response 
    if sentiment.score < 0: 
        response = "I'm sorry to hear that. We would love to hear more about your experience so that we can improve our services." 
    elif sentiment.score > 0: 
        response = "Thank you for the kind words! We really appreciate your feedback." 
    else: 
        response = "We appreciate your feedback and we're always looking to improve our services." 
    return response

