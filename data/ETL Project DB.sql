DROP DATABASE IF EXISTS restaurant_db;
CREATE DATABASE restaurant_db;

USE restaurant_db;

DROP TABLE IF EXISTS inspection;
CREATE TABLE inspection(
entry_id INT AUTO_INCREMENT NOT NULL,
restaurant_name VARCHAR(255),
restaurant_address VARCHAR(255) NOT NULL,
restaurant_city VARCHAR(45),
restaurant_state VARCHAR(2),
restaurant_zip INT(5),
health_inspection_score INT(2),
health_inspection_grade VARCHAR(1),
PRIMARY KEY (entry_id)
);

DROP TABLE IF EXISTS yelp_restaurant_data;
CREATE TABLE yelp_restaurant_data(
entry_id int(10) NOT NULL AUTO_INCREMENT,
yelp_id VARCHAR(255) NOT NULL,
yelp_rest_name VARCHAR(255),
yelp_rating FLOAT(3, 2),
yelp_review_count INT(6),
yelp_rest_address VARCHAR(255) NOT NULL,
yelp_rest_city VARCHAR(45),
yelp_rest_state VARCHAR(2),
yelp_rest_zip INT(5),
PRIMARY KEY (entry_id)
);

DROP TABLE IF EXISTS yelp_review_data;
CREATE TABLE yelp_review_data(
entry_id int(10) NOT NULL AUTO_INCREMENT,
yelp_id VARCHAR(255) NOT NULL,
yelp_rest_name VARCHAR(255),
yelp_rating FLOAT(3, 2),
yelp_review_text VARCHAR(255),
PRIMARY KEY (entry_id)
);
