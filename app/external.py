import requests
import os
import datetime
import csv
import json
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from bs4 import BeautifulSoup
from app.ml import City, validate_city
from app.state_abbr import us_state_abbrev as abbr
from dotenv import dotenv_values, load_dotenv

router = APIRouter()
load_dotenv()
weather_api = os.getenv("WEATHER_API_KEY")


# https://github.com/juhilsomaiya/API-Integrations-Python/blob/master/Weather_forecast/main.p
@router.post('/api/temperature')
async def current_weather(city:City):
    """Retrieve current weather data from openweathermap

    Fetch weather data from openweathermap
    - description
    - temperature
    - high and low
    - humidity
    - wind speed
    - real feel forecast
    - pressure

    args:
        city: The target city

    returns:
        Dictionary that contains the requested data, which is converted
        by fastAPI to a json object.

    """
    app_id = weather_api
    location = validate_city(city) # {city: "New York", state: "NY" }
    city_name = location.city + "," + location.state
    county_code = "US"
    api_call = 'http://api.openweathermap.org/data/2.5/weather?q=' + city_name + ',' + county_code + '&appid=' + app_id + '&mode=json&units=imperial'
    data = requests.post(api_call)

    data = data.json()
    main = data['main']
    today = datetime.datetime.today()
    return {
        "Date": today.strftime("%m/%d/%y"),
        "Description": data['weather'][0]['description'],
        "Temperature": str(main['temp'])+" F\N{DEGREE SIGN}",
        "High Today": str(main['temp_max'])+" F\N{DEGREE SIGN}",
        "Low Today": str(main['temp_min'])+" F\N{DEGREE SIGN}",
        "Humidity": str(main['humidity'])+ "%",
        "Wind Speed": str(data['wind']['speed'])+ " mph",
        "Feels Like": str(main['feels_like'])+" F\N{DEGREE SIGN}",
        "Pressure": str(main['pressure'])+" hPa"
    }

# https://www.youtube.com/watch?v=eN_3d4JrL_w
@router.post('/api/job_opportunities')
async def main(position, location):
    # Run the main program reouting
    records = []  # creating the record list
    url = get_url(position, location)  # create the url while passing in the position and location.

    while True:
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'jobsearch-SerpJobCard')

        for card in cards:
            record = get_record(card)
            records.append(record)

        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break

    with open('results.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Job Title', 'Company', 'Location', 'Posting Date', 'Extract Date', 'Summary', 'Salary', 'Job Url'])
        writer.writerows(records)

    csvFilePath = 'results.csv'
    jsonFilePath = 'driver.json'

    # read csv file and add to data
    data = {}
    with open(csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for rows in csvReader:
            id = rows['id']
            data[id] = rows

    # create new json file and write data on it
    with open(jsonFilePath, 'w') as jsonFile:
        # make it more readable and pretty
        jsonFile.write(json.dumps(data, indent=4))

    return jsonFile


def get_record(card):
    """Extract job date from a single record"""
    atag = card.h2.a
    job_title = atag.get('title')
    company = card.find('span', 'company').text.strip()
    job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
    job_summary = card.find('div', 'summary').text.strip()
    post_date = card.find('span', 'date').text.strip()

    try:
        salary = card.find('span', 'salarytext').text.strip()
    except AttributeError:
        salary = ''

    extract_date = datetime.datetime.today().strftime('%Y-%m-%d')
    job_url = 'https://www.indeed.com' + atag.get('href')

    record = (job_title, company, job_location, post_date, extract_date, job_summary, salary, job_url)

    return record

def get_url(position, city:City):
    "Generate a url based on position and location"

    city_name = validate_city(city)
    location = city_name.city + ' ' + city_name.state
    template = "https://www.indeed.com/jobs?q={}&l={}"
    url = template.format(position, location)
    return url

def get_record(card):
    "Exract job data from a single record"
    atag = card.h2.a
    job_title = atag.get('title')
    job_url =  'https://www.indeeed.com' + atag.get('href')
    company = card.find('span', 'company').text.strip()
    job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
    job_summary = card.find('div', 'summary').text.strip()
    post_date = card.find('span', 'date').text
    datetime.datetime.today().strftime('%Y-%m-%d')
    try:
        card.find('span', 'salaryText').text.strip()
    except AttributeError:
        job_salary = ''

    record = (job_title, company, job_location, post_date, today, job_summary, job_salary, job_url)

    return record

records = []
for card in cards:
    record = get_record(card)
    records.append(record)
