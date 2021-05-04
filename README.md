# Labs DS

[Docs](https://docs.labs.lambdaschool.com/data-science/)


## CitySpire APP:
An app that analyzes data from cities such as populations, cost of living,
rental rates, crime rates, park (walk score), and many other social
and economic factors that are important in deciding where someone would like to live.
This app will present such important data in an intuitive and easy to understand interface.
Use data to find a place right for you to live.


## DEMO
[![CitySpire 2.0 API Demo](http://img.youtube.com/vi/Rz84nk3_W54/0.jpg)](https://www.youtube.com/watch?v=Rz84nk3_W54 "CitySpire 2.0 API Demo")

## LOCAL TESTING
1. Clone repository
2.  In terminal run the following code to deploy:
    - ``pipenv install --dev``
    - ``pipenv shell``
    - ``uvicorn app.main:app --reload``
3. Go to ``localhost:8000`` in your browser, and follow the instructions you see there!
   - With the visualization endpoints, when checking locally, another tab will pop up displaying an interactive plotly graph.


## DS ENDPOINTS
http://cityspire-a.eba-tgambvt2.us-east-1.elasticbeanstalk.com/

#### Database
* /api/info
This is the link to the AWS RDS Postgres database.

* /api/all_cities
This link returns all cities covered in the database

#### Machine Learning
* /api/get_data
Here users can query cities and get an overview of the city with recommendations for similar cities
```
{
  "city": {
    "city": "San Francisco",
    "state": "CA"
  },
  "latitude": 37.773972,
  "longitude": -122.431297,
  "rental_price": 3700,
  "crime": "High",
  "air_quality_index": "Good",
  "population": 886007,
  "diversity_index": 69,
  "percent_high_performing_schools": 9,
  "walkability": 87,
  "transitscore": 80,
  "bikescore": 72,
  "livability": 52,
  "recommendations": [
    {
      "city": "Austin",
      "state": "TX"
    },
    {
      "city": "Oakland",
      "state": "CA"
    },
    {
      "city": "Portland",
      "state": "OR"
    },
    {
      "city": "San Jose",
      "state": "CA"
    },
    {
      "city": "Seattle",
      "state": "WA"
    }
  ]
}

```

* /api/coordinates
Here users can get coordinates for the city, this is used by frontend so users can visualize the city location
```

{
  "latitude": 37.775,
  "longitude": -122.4183
}

```

* /api/crime
Here users get a low, medium, high range for crime in specific cities based on the FBI crime database
```

{
  "crime": "High"
}

```

* /api/rental_price
Here users can see the estimate for rental prices in the city they are interested in
```

{
  "rental_price": 1500
}

```

* /api/pollution
This endpoint allows users to gauge the pollution based on the aqi index
```

{
  "air_quality_index": "Good"
}

```

* /api/walkability
This gives users an idea of how walkable their city is.
```

{
   "walkability": 87
}

```
* /api/transitscore
This gives users an idea of how commuter friendly their city is.
```

{
   "transitscore": 80
}
```

* /api/bikescore
This gives users an idea of how bikeable their city is.
```

{
   "walkability": 72
}

```

* /api/livability
This endpoint gives users an estimate of livability based on user preference
```

{
  "city": {
    "city": "San Francisco",
    "state": "CA"
  },
  "weights": {
    "walkability": 1,
    "bikescore": 1,
    "transitscore": 1,
    "low_rent": 1,
    "low_pollution": 1,
    "diversity": 1,
    "low_crime": 1,
    "percent_high_performing_schools": 1
  }
}

```

```

{
  "livability": 52
}

```

* /api/population
This endpoint gives users the population information for their city
```

{
  "population": 886007
}

```

* /api/school_summary
This endpoint gives a summary of school information for their city
```

{
  "total_schools": 527,
  "percent_private": 75,
  "percent_public": 22,
  "percent_charter": 3,
  "percent_high_performing_schools": 9
}

```

* /api/nearest
This endpoint allows users to find similar cities to the one they are interested in moving to
```

{
  "recommendations": [
    {
      "city": "Austin",
      "state": "TX"
    },
    {
      "city": "Oakland",
      "state": "CA"
    },
    {
      "city": "Portland",
      "state": "OR"
    },
    {
      "city": "San Jose",
      "state": "CA"
    },
    {
      "city": "Seattle",
      "state": "WA"
    }
  ]
}

```

#### Visualization
Below are the visualization endpoints that allows users to visualize and get a better sense of the cities datapoints
* /api/demographics_graph
![Demographics](https://github.com/jiobu1/labspt15-cityspire-g-ds/tree/main/notebooks/visuals/files/demographics.png)


* /api/employment_graph
![Employment](https://github.com/jiobu1/labspt15-cityspire-g-ds/tree/main/notebooks/visuals/files/employment.png)


* /api/crime_graph
![Crime Statistics](https://github.com/Lambda-School-Labs/PT17_cityspire-a-ds/blob/main/notebooks/visuals/files/crime.png)


* /api/aqi_graph
![Air Quality](https://github.com/Lambda-School-Labs/PT17_cityspire-a-ds/blob/main/notebooks/visuals/files/air_quality.png)


* /api/population_forecast_graph
![Population Forecast](https://github.com/Lambda-School-Labs/PT17_cityspire-a-ds/blob/main/notebooks/visuals/files/population.png)


* /api/rental_forecast_graph
![Rental Forecast](https://github.com/Lambda-School-Labs/PT17_cityspire-a-ds/blob/main/notebooks/visuals/files/rental_forecast.png)


#### External
Below are the external endpoints, these endpoints are either scraped or connects to another API and returns information
* /api/temperature
This endpoint connects to openweather api and returns current weather for the city

```

{
  "Date": "04/22/21",
  "Description": "broken clouds",
  "Temperature": "51.06 F°",
  "High Today": "55.4 F°",
  "Low Today": "48 F°",
  "Humidity": "71%",
  "Wind Speed": "6.91 mph",
  "Feels Like": "49.21 F°",
  "Pressure": "1015 hPa"
}

```

* /api/job_opportunities
This endpoint scrapes data from Indeed.com and returns first 10 job opportunities for the target city

```

{
  "Search Results": "1,148 jobs",
  "Top 10 Listings": [
    {
      "Job Title": "Associate Data Scientist",
      "Company": "Gap Inc.",
      "Location": "San Francisco, CA",
      "Date Posted": "2 days ago",
      "Extract Date": "2021-04-22",
      "Description": "Experience in areas of optimization, statistics and/or machine learning.\nExceptional quantitative skills with expertise in data handling.",
      "Salary": "",
      "Job Url": "https://www.indeed.com/rc/clk?jk=285f3ae1f9dff92c&fccid=76644a33987f2488&vjs=3"
    },

```

* /api/rental_listing
This endpoint connects to realtor.com and return rental information based on user input

```

{
    "Latitude": 37.775874,
    "Longitude": -122.414746,
    "Street Address": "1321 Mission St",
    "City": "San Francisco",
    "State": "California",
    "Bedrooms": 3,
    "Bathrooms": 1,
    "Cats Allowed": "Unknown",
    "Dogs Allowed": "Unknown",
    "List Price": 2750,
    "Ammenities": [
      "community_no_fee",
      "dishwasher",
      "fireplace",
      "hardwood_floors",
      "view"
    ],
    "Photos": [
      {
        "title": null,
        "description": null,
        "tags": null,
        "href": "https://ar.rdcpix.com/aa111fa785cb64592c9860350eea97a8c-f310403941o.jpg",
        "type": null
      },
      {
        "title": null,
        "description": null,
        "tags": null,
        "href": "https://ar.rdcpix.com/aa111fa785cb64592c9860350eea97a8c-f1695142536o.jpg",
        "type": null
      }
    ]
  }

```
* /api/schools_listing
This endpoint returns top 25 schools in desired city based on school category
```
{
    "School": "Children's Day School",
    "Score": 0,
    "Rating": "Currently unrated",
    "Address": "333 Dolores Street, San Francisco, CA, 94110",
    "Type": "Private",
    "Grades": "PK-8",
    "Total Students Enrolled": 441,
    "Students per teacher": "0",
    "District": "Unavailable",
    "High School (9-12)": 0,
    "Middle School (6-8)": 1,
    "Elementary (K-5)": 1,
    "Pre-Kindergarten (PK)": 1,
    "City, State": "San Francisco, CA"
  }

```


### Code Links

Below are links to resources used to create this project:

#### Models:
- Calculating Livability Index:
  https://github.com/jiobu1/labspt15-cityspire-g-ds/tree/main/notebooks/model/livability
  This is how we created the livability index for users (livability.pkl)

- Nearest Neigbhors Model:
  https://github.com/jiobu1/labspt15-cityspire-g-ds/tree/main/notebooks/model/nearest_neighbor/labs2
  This is how we created the recommendations for cities using the nearest neighbors model

- Rental Forecast
  https://github.com/jiobu1/labspt15-cityspire-g-ds/tree/main/notebooks/model/rental
  To create rental forecast, utilized 5 years of HUD fair market rental price data for studio - 3 bedrooms apartments. \
   Utilized FB Prophet on cleaned data to create a 10 year forecast of projected rental prices.

- Population Forecast
  https://github.com/jiobu1/labspt15-cityspire-g-ds/tree/main/notebooks/model/population2010_2019
  To create population forecast, utilized 10 years of census data and then utilized FB Prophet on cleaned data to create a 10 year forecast of projected rental prices.


### Feature Engineering

#### Diversity Index
The diversity indext was calculated using Simpson's Diversity Index
D = 1 - ((Σ n(n-1)/ (N(N-1))
* n = numbers of individuals of each ethnicity
* N = total number of individuals of all ethnicities
* The value of D ranges between 0 and 1

#### Air Quality Index
To determine overall air quality for each city, we used the median value and then created an algorithm that separated it based on https://www.airnow.gov/aqi/aqi-basics/ index. \
![Air Quality Index](https://github.com/jiobu1/labspt15-cityspire-g-ds/tree/main/notebooks/datasets/data/pollution/aqi_index.png)

#### Crime Rate Per 1000
Crime Rate per 1,000 inhabitants: This represents the number of Index offenses per 1,000 inhabitants.For example: What is the crime rate for a municipality with 513 Index offenses (murder, rape, robbery,aggravated assault, burglary, larceny-theft and motor vehicle theft), with a population of 8,280?
513 (Index offenses) ÷ 8,280 (population) = .061957 x 1,000 = 62.0 (crime per 1,000 inhabitants)\
https://www.njsp.org/info/ucr2000/pdf/calc_ucr2000.pdf

#### Walkability, Bikeability, Public Transportaion
To calculate walkability, bikeability, and public transportaion columns, we used the scores from the walkscore api
![Walkscore Methodology](https://www.walkscore.com/methodology.shtml)


### Datasets:
(https://github.com/jiobu1/labspt15-cityspire-g-ds/tree/main/notebooks/datasets/datasets_to_merge) \
The first link shows all combined csv that is stored in Postgres.

(https://github.com/jiobu1/labspt15-cityspire-g-ds/tree/main/notebooks/datasets/data) \
This link shows all the different datasets we used to compile our data about the different cities.


### API:
https://github.com/jiobu1/labspt15-cityspire-g-ds/tree/main/app \
This is where the code for creating the different endpoints can be located.


### Packages/Technologies used:
https://github.com/jiobu1/labspt15-cityspire-g-ds/tree/main/Pipfile


**Tech Stacks**
- Python
- SQL
- Scikit
- Beautiful Soup, requests (webscraping)
- Selenium (webscraping)
- AWS RDS PostgreSQL: Relational database service.
- AWS Elastic Beanstalk: Platform as a service, hosts your API.
- FastAPI: Web framework. Like Flask, but faster, with automatic interactive docs.
- Plotly: Visualization library, for Python & JavaScript.
- Pytest: Testing framework, runs your unit tests.


### Other Links
**Data Sources:**
* US Census - https://www.census.gov/
* FBI Crime Data - https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/tables/table-8
* Job Opportunities - http://www.indeed.com
* Pollution Data - https://aqs.epa.gov/aqsweb/airdata
* Rental Data - https://www.huduser.gov/
* Rental Listing - https://www.realtor.com/
* School Listing - https://www.greatschools.org
* Walkscore, Bikescore, Busscore -  https://www.walkscore.com/
* Weather - https://home.openweathermap.org/

| [Jisha Obukwelu](https://github.com/jiobu1) |
| :-: |
| [<img src="https://avatars.githubusercontent.com/u/54873526?s=460&u=e2d546433e06a73b443a01efce84abd6f859f071&v=4" width = "200" />](https://github.com/jiobu1) |
| [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/jiobu1) |
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/jishaobukwelu/) |

## Contributors

|                                                          [Jisha Obukwelu](https://github.com/jiobu1)                                                          |                                                       [Erik Seguinte](https://github.com/ErikSeguinte)                                                        |                                                      [dataabyss](https://github.com/dataabyss)                                                       |                                                      [Keino Baird](https://github.com/kbee181756)                                                       |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------: |
| [<img src="https://avatars.githubusercontent.com/u/54873526?s=460&u=e2d546433e06a73b443a01efce84abd6f859f071&v=4" width = "200" />](https://github.com/jiobu1) | [<img src="https://avatars.githubusercontent.com/u/16523146?s=460&u=f1fce03e1dbbea7a3dcdf7eb969a5d8ce1f88bca&v=4" width = "200" />](https://github.com/ErikSeguinte) | [<img src="https://avatars.githubusercontent.com/u/52636690?s=400&u=dc37aaaf8c0ed8f175dbce3c5917387b2e3c7bc8&v=4" width = "200" />](https://github.com/dataabyss) | [<img src="https://avatars.githubusercontent.com/u/16375650?s=400&u=3a340b63117bb7cf3bf5110df0e49c0071183975&v=4" width = "200" />](https://github.com/kbee181756) |
|                                      [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/jiobu1)                                       |                            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/ErikSeguinte)                             |                          [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/dataabyss)                           |                         [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/kbee181756)                          | [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/wvandolah) |
|                  [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/jishaobukwelu/)                  |                 [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/erik-seguinte/)                 |                [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/)                |                [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/keino-baird-7a54921b/)                |

<br>
<br>

