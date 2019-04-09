import os
import pandas as pd
import json
from sqlalchemy import create_engine
import api_key
import requests
from ratelimit import limits

headers = {"Authorization" : "Bearer" + " " + api_key.api_key}

restaurant_dict = {"id": [],
                  "name": [],
                  "address": [],
                  "city": [],
                  "state": [],
                  "zip": []}

restaurant_review_dict = {"restaurant": [],
                          "restaurant_id": [],
                         "rating": [],
                         "text": [],
                         "time_created": []}

@limits(calls=5, period=1)
def yelp_la_restaurants():
    for i in range(0, 1000, 20):
        try:
            url = "https://api.yelp.com/v3/businesses/search?term=restaurant&location=Los Angeles&limt=50&offset=" + str(i)
            restaurant_data = requests.get(url, headers=headers).json()
            restaurants = restaurant_data["businesses"]
            for j in range(0, len(restaurants)):
                restaurant_dict["id"].append(restaurants[j]["id"])
                restaurant_dict["name"].append(restaurants[j]["name"])
                restaurant_dict["address"].append(restaurants[j]["location"]["address1"])
                restaurant_dict["city"].append(restaurants[j]["location"]["city"])
                restaurant_dict["state"].append(restaurants[j]["location"]["state"])
                restaurant_dict["zip"].append(restaurants[j]["location"]["zip_code"])
                print(str(restaurants[j]["name"]))
        except:
            print("Invalid data. Skipping entry...")
            pass
    print("LA restaurant processing complete.")

yelp_la_restaurants()

restaurant_df = pd.DataFrame(restaurant_dict)
# restaurant_df

@limits(calls=5, period=1)
def yelp_reviews():
    for i in range(0, len(restaurant_dict["id"])):
        restaurant_id = restaurant_dict["id"][i]
        try:
            url = "https://api.yelp.com/v3/businesses/" + restaurant_id + "/reviews"
            restaurant_review_data = requests.get(url, headers=headers).json()
            reviews = restaurant_review_data["reviews"]
            for j in range(0, len(reviews)):
                restaurant_review_dict["restaurant"].append(restaurant_dict["name"][i])
                restaurant_review_dict["restaurant_id"].append(restaurant_dict["id"][i])
                restaurant_review_dict["rating"].append(reviews[j]["rating"])
                restaurant_review_dict["text"].append(reviews[j]["text"])
                restaurant_review_dict["time_created"].append(reviews[j]["time_created"])
            print("Top 3 reviews for " + str(restaurant_dict["name"][i]) + " completed.")
            print("---------------------------------------------------------------------")
        except:
            print("Business ID is invalid. Skipping invalid business data...")
            pass

    print("Yelp Reviews API process completed.")

yelp_reviews()

reviews_df = pd.DataFrame(restaurant_review_dict)
# reviews_df

reviews_copy = reviews_df.copy().drop_duplicates(keep="first")
restaurants_copy = restaurant_df.copy().drop_duplicates(keep="first")

reviews_copy.to_csv("yelp_reviews.csv", header=True)
restaurants_copy.to_csv("yelp_la_restaurants.csv", header=True)
