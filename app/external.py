from fastapi import APIRouter, HTTPException, Depends
import requests
import datetime
import time
import os
from pydantic import BaseModel
from app.ml import City, validate_city
from app.state_abbr import us_state_abbrev as abbr
from dotenv import dotenv_values, load_dotenv

router = APIRouter()
load_dotenv()
weather_api = os.getenv("WEATHER_API_KEY")



# 3 https://github.com/juhilsomaiya/API-Integrations-Python/blob/master/Weather_forecast/main.p
@router.post('/api/temperature')
def get_data():
    app_id = weather_api
    details = get_details()
    city_name = details.get('city')
    county_code = details.get('county')
    api_call = 'http://api.openweathermap.org/data/2.5/forecast?q=' + city_name + ',' + county_code + '&appid=' + app_id + '&mode=json&units=imperial'
    print(api_call)
    data = requests.post(api_call)
    date = []
    temp = []
    high = []
    low = []
    humidity = []
    wind_speed = []
    real_feel = []
    pressure = []
    desc = []

    data = data.json()
    for lists in data['list']:
        date.append(lists['dt_txt'])
        temp.append(lists['main']['temp'])
        high.append(lists['main']['temp_max'])
        high.append(lists['main']['temp_min'])
        humidity.append(lists['main']['humidity'])
        wind_speed.append(lists['wind']['speed'])
        real_feel.append(lists['main']['feels_like'])
        pressure.append(lists['main']['pressure'])
        desc.append(lists['weather'][0]['description'])


    result = []
    for i in range(len(humidity)):
        print(len(humidity))
    result.append({
        "Date": str(date[i]),
        "Description": desc[i],
        "Temperature": str(temp[i])+" F\N{DEGREE SIGN}",
        "High Today": str(high[i])+" F\N{DEGREE SIGN}",
        "Low Today": str(temp[i])+" F\N{DEGREE SIGN}",
        "Humidity": str(humidity[i])+ " %",
        "Wind Speed": str(wind_speed[i])+ " mph",
        "Feels Like": str(real_feel[i])+" F\N{DEGREE SIGN}",
        "Pressure": str(pressure[i])+" hPa"
    })
    return result

def get_details():
    city_name =  "New York"#input("Enter city name: ")
    county_code = "US" #input("Enter state name: ")
    return {'city': city_name, 'county': county_code}

# # 4 afternerd
# class WeatherParams:
#     def __init__(self, city, units="imperial", lang="en"):
#         self.city = city
#         self.units = units
#         self.lang = lang
#         self.mode = "json"

# def get_weather(appid, weather_params):
#     endpoint = "http://api.openweathermap.org/data/2.5/weather"
#     query_params = {
#         'q': weather_params.city,
#         'units': weather_params.units,
#         'lang': weather_params.lang,
#         'mode': weather_params.mode,
#         'appid': appid,
#     }
#     resp = requests.get(endpoint, params=query_params)
#     return resp.json

# @router.post("/api/walkability")
# async def get_walkability(city: City):
#     """Retrieve walkscore for target city

#     args:
#         city: The target city

#     returns:
#         Dictionary that contains the requested data, which is converted
#         by fastAPI to a json object.
#     """
#     city = validate_city(city)
#     try:
#         score = (await get_walkscore(**city.dict()))[0]
#     except IndexError:
#         raise HTTPException(
#             status_code=422, detail=f"Walkscore not found for {city.city}, {city.state}"
#         )

#     return {"walkability": score}


# async def get_walkscore(city: str, state: str):
#     """Scrape Walkscore.

#     args:
#         city: The target city
#         state: Target state as an all-caps 2-letter abbr

#     returns:
#         List containing WalkScore, BusScore, and BikeScore in that order
#     """

#     r_ = requests.get(f"https://www.walkscore.com/{state}/{city}")
#     images = bs(r_.text, features="lxml").select(".block-header-badge img")
#     return [int(str(x)[10:12]) for x in images]