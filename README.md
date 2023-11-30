# flask_ACNH_backend
flask_ACNH_backend project is created to get back end REST API end points to get vilagers of animal crossing new horizons game

In db_client.py, create database connection to connect with SQL server (2019) and some funton to load data from database( get villagers...)

db_scraper.py is created to scrape data from website https://animalcrossing.fandom.com/wiki/Villager_list_(New_Horizons) using Beautiful Soup
(Python package for parsing HTML and XML documents)

app.py is the main flask app which includes where to look for resources, which URLs should trigger our functions

In the requirement.txt has included what python packages are required to run this project
