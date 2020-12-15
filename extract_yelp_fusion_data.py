# Native
import os
import json

# Third party
import requests
import pandas as pd
from sqlalchemy import create_engine
from ratelimit import limits

# Custom
from config import yelp_api_key


# Yelp Fusion API requires api keys to be passed through HTTP header value:
headers = {"Authorization" : "Bearer" + " " + yelp_api_key}


@limits(calls=5, period=1)
def get_yelp_la_restaurants():
    """A function that makes an API call to retrieve information on restaurants in LA then appends said data to relevant dictionary
    values. The "@limits" decorator ensures api calls don't exceed calls-per-second limit.
    """
    LA_restaurants_dict = {"id": [],
                  "name": [],
                  "overall_rating": [],
                  "review_count": [],
                  "address": [],
                  "city": [],
                  "state": [],
                  "zip": []}
    restaurants_processed_count = 0
    
    for i in range(0, 1000, 20):
        try:
            url = "https://api.yelp.com/v3/businesses/search?term=restaurant&location=Los Angeles&limt=50&offset=" + str(i)
            restaurant_data = requests.get(url, headers=headers).json()
            restaurants = restaurant_data["businesses"]
            for j in range(0, len(restaurants)):
                LA_restaurants_dict["id"].append(restaurants[j]["id"])
                LA_restaurants_dict["name"].append(restaurants[j]["name"])
                LA_restaurants_dict["overall_rating"].append(restaurants[j]["rating"])
                LA_restaurants_dict["review_count"].append(restaurants[j]["review_count"])
                LA_restaurants_dict["address"].append(restaurants[j]["location"]["address1"])
                LA_restaurants_dict["city"].append(restaurants[j]["location"]["city"])
                LA_restaurants_dict["state"].append(restaurants[j]["location"]["state"])
                LA_restaurants_dict["zip"].append(restaurants[j]["location"]["zip_code"])
                restaurants_processed_count += 1
                print(f'{restaurants_processed_count}.) {restaurants[j]["name"]} is now being stored.')
        except:
            print("Invalid data. Skipping entry...")
            pass
        
    print("\n----------------------------LA restaurant processing complete.----------------------------\n")
    return LA_restaurants_dict

# Calls and logs API calls (LA restaurant data) to Yelp Fusion  
LA_restaurants_dict = get_yelp_la_restaurants()
LA_restaurants_df = pd.DataFrame(LA_restaurants_dict)


@limits(calls=5, period=1)
def get_yelp_reviews(LA_restaurants_dict):
    """A function that makes API calls to Yelp Fusion to retrieve review data for the businesses with business id's stored in the
    "restaurant_dict" above then appends retrieved review data to "restaurant_review_dict".
    """
    LA_restaurant_reviews_dict = {"restaurant": [],
                          "restaurant_id": [],
                         "rating": [],
                         "text": [],
                         "time_created": []}
    reviews_processed_count = 0
    
    for i in range(0, len(LA_restaurants_dict["id"])):
        restaurant_id = LA_restaurants_dict["id"][i]
        try:
            url = "https://api.yelp.com/v3/businesses/" + restaurant_id + "/reviews"
            restaurant_review_data = requests.get(url, headers=headers).json()
            reviews = restaurant_review_data["reviews"]
            for j in range(0, len(reviews)):
                LA_restaurant_reviews_dict["restaurant"].append(LA_restaurants_dict["name"][i])
                LA_restaurant_reviews_dict["restaurant_id"].append(LA_restaurants_dict["id"][i])
                LA_restaurant_reviews_dict["rating"].append(reviews[j]["rating"])
                LA_restaurant_reviews_dict["text"].append(reviews[j]["text"])
                LA_restaurant_reviews_dict["time_created"].append(reviews[j]["time_created"])
            reviews_processed_count += 1
            print(f'{reviews_processed_count}.) Top 3 reviews for {LA_restaurants_dict["name"][i]} completed.')
            print("---------------------------------------------------------------------")
        except:
            print("Business ID is invalid. Skipping invalid business data...")
            pass

    print("\n----------------------------Yelp Reviews API process completed.----------------------------\n")
    return LA_restaurant_reviews_dict


LA_restaurant_reviews_dict = get_yelp_reviews(LA_restaurants_dict)
LA_restaurant_reviews_df = pd.DataFrame(LA_restaurant_reviews_dict)

# Drop duplicate data
LA_restaurants_df_copy = LA_restaurants_df.copy().drop_duplicates(keep="first")
LA_restaurant_reviews_df_copy = LA_restaurant_reviews_df.copy().drop_duplicates(keep="first")

# Create CSVs
LA_restaurants_df_copy.to_csv("yelp_LA_restaurants.csv", header=True)
LA_restaurant_reviews_df_copy.to_csv("yelp_LA_reviews.csv", header=True)