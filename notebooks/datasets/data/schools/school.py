#reference: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup
import os
import requests
import csv
import json
import pandas as pd
from state_abbr import us_state_abbrev as abbr
from selenium import webdriver
import urllib.parse

# 1. Create full state name/ city column to use in getting school information
pwd = os.getcwd()

# create city state list
cities = pd.read_excel('notebooks/datasets/data/schools/csv/List of Cities.xlsx')

# just get the second and third colun
cities = cities[['Unnamed: 1','Unnamed: 2']]

# create new dictionary with reversed key, value pairs
full = dict(map(reversed, abbr.items()))

# map state abbreviations to full name
cities['states'] = cities['Unnamed: 2'].map(full)

# making sure state/city combo conform to url format of "-" for " "
cities['states'] = cities['states'].str.strip()
cities['states'] = cities['states'].str.replace(" ", "-")
cities['Unnamed: 1'] = cities['Unnamed: 1'].str.replace(" ", "-")

# remove extraneous header rows
cities = cities.iloc[2:]
cities['city'] = (cities['states'] + '/'+ cities['Unnamed: 1']).str.lower()
print(cities.head())

# persist by creating new csv
cities.to_csv('notebooks/datasets/data/schools/csv/cities.csv')

# 2. using selenium to get school information
driver = webdriver.Chrome()

# 3. url for greatschools pre_url and post_url (with state/city inbetween)
url_pre = "http://www.greatschools.org/"
url_post = "/schools/?tableView=Overview&view=table"

# Call cities csv to get cities stored in database
cities = pd.read_csv('notebooks/datasets/data/schools/csv/cities.csv')


# 4. Looping through each city in the file
# create empty dataframe
df = pd.DataFrame()

for i in cities['city']:
    endpoint = url_pre + urllib.parse.quote(i) + url_post
    print("Fetching ", endpoint)
    driver.get(endpoint)
    html = driver.page_source
    table = pd.read_html(html)
    # appending to dataframe all the schhol information for current cities
    df = df.append(table[0])

driver.close()

# 5. For persisitance creating a schools csv
df.to_csv('notebooks/datasets/data/schools/csv/schools.csv')