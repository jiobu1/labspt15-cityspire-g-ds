import requests
import os
import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, SecretStr
from bs4 import BeautifulSoup
from app.ml import City, validate_city
from app.state_abbr import us_state_abbrev as abbr
from app import config
from dotenv import dotenv_values, load_dotenv

router = APIRouter()
load_dotenv()



class Settings(BaseSettings):

    RENTAL_API_KEY: SecretStr


    class Config:
        env_file = ".env"

settings = Settings()


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
# https://medium.com/@hannah15198/convert-csv-to-json-with-python-b8899c722f6d
@router.post('/api/job_opportunities')
async def job_opportunities(position, city:City):
    """Returns jobs opportunities from indeed.com

    Fetch first 10 job opportunities
    - Job title,
    - Company,
    - Job location
    - Post Date,
    - Extract Date,
    - Job Description,
    - Salary,
    - Job Url

    args:
        - position: desired job opportunity
        - city: target city

    returns:
        Dictionary that contains the requested data, which is converted
        by fastAPI to a json object.

    """
    # Run the main program reouting
    records = []  # creating the record list

    city_name = validate_city(city)
    location = city_name.city + ' ' + city_name.state
    url = get_url(position, location)  # create the url while passing in the position and location.

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', 'jobsearch-SerpJobCard')

    for card in cards:
        record = get_record(card)
        records.append(record)

    #also return total number of jobs
    try:
        total_jobs = soup.find('div', id='searchCountPages').text.strip()
        total = total_jobs.split()[-2:]
        jobs = ' '.join(total)
    except AttributeError:
        total_jobs = ''
        jobs = ''

    return {"Search Results":jobs, "Top 10 Listings": records}

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

    record = {'Job Title': job_title,
              'Company': company,
              'Location': job_location,
              'Date Posted': post_date,
              'Extract Date': extract_date,
              'Description': job_summary,
              'Salary': salary,
              'Job Url': job_url}

    return record

def get_url(position, location):
    "Generate a url based on position and location"

    template = "https://www.indeed.com/jobs?q={}&l={}"
    url = template.format(position, location)
    return url


# @router.post('api/rental_listing')
# async def api_property_list_for_rent(city:City, api_key = settings.RENTAL_API_KEY, prop_type = 'condo', limit=4): #os.getenv("RENTAL_API_KEY")

#     # url for api
#     url = "https://realtor-com-real-estate.p.rapidapi.com/for-rent"

#     # enter parameters
#     querystring = {
#         'sort' : 'relevance',
#         'city' : city,
#         'offset' : '0',
#         'limit': limit,
#         'prop_type' : prop_type
#     }

#     # header
#     headers = {
#         'x-rapidapi-key': os.getenv("RENTAL_API_KEY"),
#         'x-rapidapi-host': "realtor-com-real-estate.p.rapidapi.com"
#         }


#     # response
#     # fetch = window.fetch.bind(window)
#     response = requests.request("GET", url, headers=headers, params=querystring)
#     print(url)

#     print(response.text)
#     return response.json()

#     # rental_list = []

#     # for i in response['properties']:
#     #     rental_list.append(i)

#     # return rental_list

# import requests

# url = "https://realtor-com-real-estate.p.rapidapi.com/for-rent"

# querystring = {"city":"Detroit","state_code":"MI","limit":"42","offset":"0"}

# headers = {
#     'x-rapidapi-key': os.getenv("RENTAL_API_KEY"),
#     'x-rapidapi-host': "realtor-com-real-estate.p.rapidapi.com"
#     }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(type(response.text))

headers={'x-rapidapi-key': os.getenv('RENTAL_API_KEY'),
            'x-rapidapi-host':  "realtor-com-real-estate.p.rapidapi.com"}



@router.post('/streamlined_rent_list')
async def streamlined_rent_list(
            #  city: str="New York City",
            #  state: str="NY",
            city:City,
            api_key=settings.RENTAL_API_KEY,
            prop_type: str="condo",
            limit: int=1):

    """
    Parameters:
        api_key
        city: str
        state: str Two-letter abbreviation
        prop_type: str ('condo', 'single_family', 'multi_family')
        limit: int number of results to populate

    Returns: dict
        Chosen information of the requested parameters such
        as addresses, state, ciy, lat, lon, photos, walk score, pollution info
    """

    city = validate_city(city)
    location_city = city.city
    location_state = city.state

    url="https://realtor-com-real-estate.p.rapidapi.com/for-rent"
    querystring={
                "city": location_city,
                "state_code" : location_state,
                "limit": limit,
                "offset": "0",
                "sort":"relevance",
                "prop_type": prop_type}

    response_for_rent=requests.request("GET", url, params=querystring, headers=headers,)
    response = response_for_rent.json()['data']['results']
    # pollution_res = pollution(city)
    # print(response.keys())

    # rental_list=[]
    # for i in range(limit):
    #   line=response[i]['address']['line']
    #   city=response[i]['address']['city']
    #   state=response[i]['address']['state']
    #   lat=response[i]['address']['lat']
    #   lon=response[i]['address']['lon']
    #   photos=response[i]['photos']
    #   element={ 'lat': lat,
    #             'lon': lon,
    #             'city':city,
    #             'state':state,
    #             'photos': photos}
    #             # 'pollution': pollution_res}


    #   rental_list.append(element)

    # return rental_list

    return response