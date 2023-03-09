# create a python program to read google maps reviews and store them in a csv file
# import the required libraries
import os
import requests
import json
import csv
import time


# define the constants
API_KEY = os.environ.get("GOOGLEAPIKEY")
PLACE_ID = "ChIJmQa2NZUrdTERWx3Ui77zN0c"
URL_START = "https://maps.googleapis.com/maps/api/place/details/json?"
# define the function to get the reviews


def get_reviews(url):
    # get the response from the url
    response = requests.get(url, timeout=5)
    # convert the response to json format
    json_data = json.loads(response.text)
    # return the json data
    return json_data


# define the function to write the reviews to a csv file
def write_reviews_to_csv(json_data, file_name):
    # open the file in write mode
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        # create a csv writer object
        writer = csv.writer(file)
        # write the header
        writer.writerow(
            ['author_name', 'rating', 'relative_time_description', 'text'])
        # write the data
        # print(json_data)
        for review in json_data:
            writer.writerow([review['author_name'], review['rating'],
                            review['relative_time_description'], review['text']])


# define the main function
def main():
    # get the url
    url = f'{URL_START}placeid={PLACE_ID}&fields=reviews&reviews_sort=newest&key={API_KEY}'
    print(url)
    # write the reviews to a csv file
    write_reviews_to_csv(get_reviews(url), 'reviews.csv')


# call the main function
if __name__ == '__main__':
    main()
