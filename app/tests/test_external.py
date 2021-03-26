import requests
import json
from jsonschema import validate
from jsonschema import Draft6Validator

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
    "Date": "string",
    "Description": "string",
    "Temperature": "string",
    "High": "string",
    "Low": "string",
    "Humidity": "string",
    "Wind_Speed": "string",
    "Feels_Like": "string",
    "Pressure": "string"
}

def test_weather_data_validates_json_resonse_schema():
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

def test_job_opportunities_validates_json_resonse_schema():
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