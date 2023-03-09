from google.cloud import language_v1
import os

API_KEY = os.environ.get("GOOGLEAPIKEY")

# Instantiate the client
client = language_v1.LanguageServiceClient()

# Define the text to analyze
text = u'This is a great restaurant! The service was amazing and the food was delicious.'

# Define document type and encoding
document = {'content': text, 'type': language_v1.Document.Type.PLAIN_TEXT}

# Analyze the sentiment of the text
encoding_type = language_v1.EncodingType.UTF8

Entity_response = client.analyze_entities(request={"document": document, "encoding_type": encoding_type})
Sentiment_response = client.analyze_sentiment(request={"document": document})

# Print the sentiment score and magnitude
sentiment = Sentiment_response.document_sentiment
print('Sentiment score: {:.2f}'.format(sentiment.score))
print('Sentiment magnitude: {:.2f}'.format(sentiment.magnitude))
