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

# 1
def temperature():
    query = request.form['q']
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+query+',us&appid='+weather_api)
    json_object = r.json()
    temp_k = float(json_object['main']['temp'])
    temp_f = (temp_k - 273.15) * 1.8 + 32
    return {"current temperature": temp_f}

# 2
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