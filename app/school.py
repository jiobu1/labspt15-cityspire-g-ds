#reference: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup
import os
import requests
import csv
import json
import pandas as pd


pwd = getcwd()

cities = pd.read_excel('List of Cities.xlsx')
cities = cities[['Unnamed: 1','Unnamed: 2']]
cities = cities.iloc[2:]
cities['city'] = cities['Unnamed: 1'] + '/'+ cities['Unnamed: 2']

cities.to_csv('cities.csv')