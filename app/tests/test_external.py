import os
import requests
import json
from jsonschema import validate
from jsonschema import Draft6Validator
from dotenv import dotenv_values, load_dotenv

load_dotenv()

#Weather API Test
def test_temperature_check_status_code_equals_200():
    data = {
        "city": "New York",
        "state": "NY"
    }
    response = requests.post("http://127.0.0.1:8000/api/temperature", json=data)
    assert response.status_code == 200

weather_schema = {
    "$schema": "https://json-schema.org/schema#",
    "city": {
        "city": "New York",
        "state": "NY"
    },
    "Date": str,
    "Description": str,
    "Temperature": str,
    "High": str,
    "Low": str,
    "Humidity": str,
    "Wind_Speed": str,
    "Feels_Like": str,
    "Pressure": str
}

def test_weather_data_validates_json_response_schema():
    data = {
        "city": "New York",
        "state": "NY"
    }
    response = requests.post("http://127.0.0.1:8000/api/temperature", json=data)

    # Validate response headers and body contents, e.g. status code.
    assert response.status_code == 200

    # Validate response content type header
    assert response.headers["Content-Type"] == "application/json"

    resp_body = response.json()

    # Validate will raise exception if given json is not
    # what is described in schema.
    validate(instance=resp_body, schema=weather_schema)

##########################################################################################################

# Job Opportunities Test
def test_job_opportunities_check_status_code_equals_200():
    data = {
        "city": "New York",
        "state": "NY"
    }
    response = requests.post("http://127.0.0.1:8000/api/job_opportunities?position=senior+accountant", json=data)
    assert response.status_code == 200

job_opportunities_schema = {
    "$schema": "https://json-schema.org/schema#",
    "city": {
        "city": "New York",
        "state": "NY"
    },
    "Job Title": str,
    "Company": str,
    "Location": str,
    "Date Posted": str,
    "Extract Date": str,
    "Description": str,
    "Salary": str,
    "Job Url": str
}

def test_job_opportunities_validates_json_response_schema():
    data = {
        "city": "New York",
        "state": "NY"
    }
    response = requests.post("http://127.0.0.1:8000/api/job_opportunities?position=senior+accountant", json=data)

    # Validate response headers and body contents, e.g. status code.
    assert response.status_code == 200

    # Validate response content type header
    assert response.headers["Content-Type"] == "application/json"

    resp_body = response.json()

    # Validate will raise exception if given json is not
    # what is described in schema.
    validate(instance=resp_body, schema=job_opportunities_schema)

##########################################################################################################

# Rental Listing Test
def test_rental_listing_check_status_code_equals_200():
    data = {
        "api_key": os.getenv("RENTAL_API_KEY"),
        "city": "New York",
        "state": "NY",
        "beds_min": int=1,
        "baths_min": int=1,
        "prop_type" : "apartment",
        "limit" : 5
    }
    response = requests.post("http://127.0.0.1:8000/api/rental_listing?", json=data)

rental_listings_schema = {
    "$schema": "https://json-schema.org/schema#",
    "Latitude" : "number",
    "Longitude" : "number",
    "Street Address" : "string",
    "City" : "string",
    "State" : "string",
    "Bedrooms" : "integer",
    "Bathrooms" : "integer",
    "Cats Allowed" : "boolean",
    "Dogs Allowed" : "boolean",
    "List Price": "integer",
    "Ammenities" : "array",
    "Photos" : "array",
}

def test_rental_listing_validates_json_response_schema():
    data = {
        "api_key": os.getenv("RENTAL_API_KEY"),
        "city": "New York",
        "state": "NY",
        "beds_min": int=1,
        "baths_min": int=1,
        "prop_type" : "apartment",
        "limit" : 5
    }
    response = requests.post("http://127.0.0.1:8000/api/rental_listing?", json=data)

    # Validate response headers and body contents, e.g. status code.
    assert response.status_code == 200

    # Validate response content type header
    assert response.headers["Content-Type"] == "application/json"

    resp_body = response.json()

    # Validate will raise exception if given json is not
    # what is described in schema.
    validate(instance=resp_body, schema=rental_listings_schema)