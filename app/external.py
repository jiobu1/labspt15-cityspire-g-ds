from fastapi import APIRouter, HTTPException, Depends
import requests
from pydantic import BaseModel
from app.ml import City, validate_city
from app.state_abbr import us_state_abbrev as abbr
from dotenv import dotenv_values, load_dotenv

router = APIRouter()
load_dotenv()
weather_api = os.getenv("WEATHER_API_KEY")


@router.post('/api/temperature')

# 1 https://www.w3resource.com/python-exercises/web-scraping/web-scraping-exercise-21.php
def temperature():
    query = request.form['q']
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+query+',us&appid='+weather_api)
    json_object = r.json()
    temp_k = float(json_object['main']['temp'])
    temp_f = (temp_k - 273.15) * 1.8 + 32
    return {"current temperature": temp_f}

# 2  https://github.com/PrettyPrinted/python-weather-api/blob/master/test.py
def weather_data(query):
	res=requests.get('http://api.openweathermap.org/data/2.5/weather?'+query+',us&appid='+weather_api);
	return res.json()

def print_weather(result,city):
	print("{}'s temperature: {}°C ".format(city,result['main']['temp']))
	print("Wind speed: {} m/s".format(result['wind']['speed']))
	print("Description: {}".format(result['weather'][0]['description']))
	print("Weather: {}".format(result['weather'][0]['main']))

def main():
	city=input('Enter the city:')
	print()
	try:
	  query='q='+city;
	  w_data=weather_data(query);
	  print_weather(w_data, city)
	  print()
	except:
	  print('City name not found...')

if __name__=='__main__':
	main()

import requests
import datetime
import time

cronjob = True

# 3 https://github.com/juhilsomaiya/API-Integrations-Python/blob/master/Weather_forecast/main.py
def get_details():
    city_name = input("Enter city name")
    country_code = input("Enter country code")
    return {'city': city_name, 'country_code': country_code}


def get_data():
    app_id = 'Replace with yours'
    details = get_details()
    city_name = details.get('city')
    country_code = details.get('country_code')
    api_call = 'http://api.openweathermap.org/data/2.5/forecast?q=' + city_name + ',' + country_code + '&appid=' + app_id + '&mode=json&units=metric'

    data = requests.post(api_call)
    humidity = []
    date = []
    temp = []
    desc = []
    pressure = []
    sea_level = []

    data = data.json()
    print("\t" + "Details about the forcast of the city " + city_name + " of next 5 days " + "\n\n")
    for lists in data['list']:
        date.append(lists['dt_txt'])
        humidity.append(lists['main']['humidity'])
        temp.append(lists['main']['temp'])
        pressure.append(lists['main']['pressure'])
        sea_level.append(lists['main']['sea_level'])
        desc.append(lists['weather'][0]['description'])

    print('{:^25}{:^20}{:^20}{:^20}{:^20}{:^20}'.format("Date", "Description", "Temprature", "Humidity", "Pressure", "Sea_level\n"))
    for i in range(len(humidity)):
        print('{:^25}{:^20}{:^20}{:^20}{:^20}{:^20}'.format(str(date[i]), desc[i], str(temp[i])+" C\N{DEGREE SIGN}", str(humidity[i])+" %",
            str(pressure[i])+" hPa", str(sea_level[i])+" hPa"))

    with open("test.txt", "a+") as file:
        date = datetime.datetime.now().strftime("%H:%M:%S")
        file.write('Logged data at: ' + str(date) + '\n')

    if cronjob:
        time.sleep(5)
        get_data()


get_data()

# 4 afternerd
class WeatherParams:
    def __init__(self, city, units="imperial", lang="en"):
        self.city = city
        self.units = units
        self.lang = lang
        self.mode = "json"

def get_weather(appid, weather_params):
    endpoint = "http://api.openweathermap.org/data/2.5/weather"
    query_params = {
        'q': weather_params.city,
        'units': weather_params.units,
        'lang': weather_params.lang,
        'mode': weather_params.mode,
        'appid': appid,
    }
    resp = requests.get(endpoint, params=query_params)
    return resp.json

@router.post("/api/walkability")
async def get_walkability(city: City):
    """Retrieve walkscore for target city

    args:
        city: The target city

    returns:
        Dictionary that contains the requested data, which is converted
        by fastAPI to a json object.
    """
    city = validate_city(city)
    try:
        score = (await get_walkscore(**city.dict()))[0]
    except IndexError:
        raise HTTPException(
            status_code=422, detail=f"Walkscore not found for {city.city}, {city.state}"
        )

    return {"walkability": score}


async def get_walkscore(city: str, state: str):
    """Scrape Walkscore.

    args:
        city: The target city
        state: Target state as an all-caps 2-letter abbr

    returns:
        List containing WalkScore, BusScore, and BikeScore in that order
    """

    r_ = requests.get(f"https://www.walkscore.com/{state}/{city}")
    images = bs(r_.text, features="lxml").select(".block-header-badge img")
    return [int(str(x)[10:12]) for x in images]