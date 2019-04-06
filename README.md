# Project2
• Your two data sets
• A preliminary sketch of your database (type of DB, tables, etc)
• Preliminary list of necessary data transformations

ETL project group: Heather Leek, Theodore Moreland, Adam Feldstein

We will be utilizing the following data sources from Kaggle.com:
https://www.kaggle.com/cityofLA/la-restaurant-market-health-data
https://www.kaggle.com/yelp-dataset/yelp-dataset
  yelp_academic_dataset_review.json
  yelp_academic_dataset_business.json

The first data set provides information about restaurants in Los Angeles, CA along with their name, address, city, state, zip and inspection health grade and health grade percentage.  The Yelp data will be an academic data set with reviews and star rating along with restaurant data.  

We intend to use a SQL database with the following tables:

Health Data Table:        
Restaurant Name
Restaurant Address
Restaurant City
Restaurant State
Restaurant Zip
Health Inspection Score
Health Inspection Grade

Yelp Restaurant Table 
Business ID
Business Name
Business Address
Business City
Business State
Business Zip

Yelp Star Rank Table
Business ID
Star Rating
Review data

Transformations:
We will take each data set and reduce them to necessary fields only in a Jupyter notebook.
We will clean fields in each data set to ensure they appropriate.  For example, some of the zip codes are the full postal with 5-4 and some are just the the 5 numbers.
We will create new dataframes from each data set in preparation for the SQL database.  
