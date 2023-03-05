# import json
# import requests from google.cloud
# import language from google.cloud.language
# import enums from google.cloud.language
# import types 
# #Google Review Responder
# def google_review_responder(text): 
# nitialize the Google Natural Language API 
# client = language.LanguageServiceClient() 
# # Analyze the sentiment of the text document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT) 
# sentiment = client.analyze_sentiment(document=document).document_sentiment 
# # Generate the response if sentiment.score < 0: 
# response = "I'm sorry to hear that. We would love to hear more about your experience so that we can improve our services." 
# elif sentiment.score > 0: 
# response = "Thank you for the kind words! We really appreciate your feedback." 
# else: 
# response = "We appreciate your feedback and we're always looking to improve our services." 
# return response ``


import requests 
# Get all the google business reviews posted in the last hour 
# url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=reviews&key=YOUR_API_KEY'
# response = requests.get(url)
# business_reviews = response.json()
# # Loop through each review for review in business_reviews['result']['reviews']:
# # Get the time the review was posted in milliseconds
# review_time = review['time'] 
# If the review was posted in the last hour if review_time >= (time.time() * 1000) - 3600000:
# # Do something with the review print(review) ``