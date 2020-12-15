# Native
import os.path as os

# Third party
import pandas as pd
from sqlalchemy import create_engine

# Custom
from db_access import db_user, db_pass, db_address


# # Creating Dataframes
inspection_path = os.join(".","restaurant_inspections_clean.csv")
inspection_df = pd.read_csv(inspection_path, encoding="latin-1")

yelp_restaurant_path = os.join(".","yelp_la_restaurants.csv")
yelp_restaurant_df = pd.read_csv(yelp_restaurant_path, encoding="latin-1")

yelp_review_path = os.join(".","yelp_reviews.csv")
yelp_review_df = pd.read_csv(yelp_review_path, encoding="latin-1")

# # Preparing Inspection Table
column_names = {"Restaurant ID":"restaurant_id", "Restaurant Name":"restaurant_name", 
                "Restaurant Address":"restaurant_address", "Restaurant City":"restaurant_city", 
                "Restaurant State":"restaurant_state", "Restaurant ZIP": "restaurant_zip", 
                "Health Inspection Score":"health_inspection_score", "Health Inspection Grade":"health_inspection_grade"}
inspection_df.rename(columns=column_names, inplace=True)
inspection_df.drop(axis=1, labels=["restaurant_id"], inplace=True)


# # Preparing Yelp Review Table
yelp_review_df.drop(axis=1, labels="Unnamed: 0", inplace=True)
yelp_review_df.drop(axis=1, labels="time_created", inplace=True)
column_names = {"id":"yelp_id", "name":"yelp_rest_name", 
                "rating":"yelp_rating", "text":"yelp_review_text"}
yelp_review_df.rename(columns=column_names, inplace=True)


# # Preparing Yelp Restaurant Table
yelp_restaurant_df.drop(axis=1, labels=["Unnamed: 0"], inplace=True)
column_names = {"id":"yelp_id", "name":"yelp_rest_name", "overall_rating":"yelp_rating", 
                "review_count":"yelp_review_count", "address":"yelp_rest_address", 
                "city":"yelp_rest_city", "state":"yelp_rest_state", "zip": "yelp_rest_zip"}
yelp_restaurant_df.rename(columns=column_names, inplace=True)
yelp_restaurant_df.dropna(subset=["yelp_rest_address"], inplace=True)


# # Verifying Connection to MySQL Database
connection_string = f"{db_user}:{db_pass}@{db_address}/restaurant_db"
engine = create_engine(f"mysql://{connection_string}")
engine.table_names()


# # Loading Dataframes Into Database
inspection_df.to_sql(name='inspection', con=engine, if_exists='replace', index=True)
yelp_restaurant_df.to_sql(name='yelp_restaurant_data', con=engine, if_exists='replace', index=True)
yelp_review_df.to_sql(name='yelp_review_data', con=engine, if_exists='replace', index=True)