import os
import requests
import json
from jsonschema import validate
from jsonschema import Draft6Validator

#All Cities Test
def test_temperature_check_status_code_equals_200():

    response = requests.get("http://127.0.0.1:8000/all_cities")
    assert response.status_code == 200

all_cities_schema = {
    "$schema": "https://json-schema.org/schema#",
    "city": "string",
    "state": "string"

}

def test_weather_data_validates_json_resonse_schema():

    response = requests.get("http://127.0.0.1:8000/all_cities")

    # Validate response headers and body contents, e.g. status code.
    assert response.status_code == 200

    # Validate response content type header
    assert response.headers["Content-Type"] == "application/json"

    resp_body = response.json()

    # Validate will raise exception if given json is not
    # what is described in schema.
    validate(instance=resp_body, schema=all_cities_schema)