"""Data visualization functions"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from app.ml import City, validate_city
from app.data.files.state_abbr import us_state_abbrev as abbr

router = APIRouter()

MODEL_CSV = 'https://media.githubusercontent.com/media/CityScape-Datasets/Workspace_Datasets/main/Models/nn_model/nn_model.csv'

class CityData():
    """
    Locates specific city data
    - Demographics
    - Employement -> industry, employment
    - Crime -> violent crime, property crime
    - Air Quality Index
    """

    def __init__(self, current_city):
        self.current_city = current_city
        self.dataframe = pd.read_csv(MODEL_CSV)
        self.subset = self.dataframe[self.dataframe['City'] == self.current_city.city]

    def demographics(self):
        self.demographics = ['Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific']
        return ['Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific']

    def industry(self):
        self.industry = ['PrivateWork', 'PublicWork', 'SelfEmployed', 'FamilyWork']
        return self.industry

    def employment(self):
        self.employment= ['Professional', 'Service', 'Office', 'Construction',	'Production']
        return self.employment

    def crime(self):
        self.crime = ['Violent crime', 'Property crime', 'Arson']
        return self.crime

    def violent_crime(self):
        self.violent_crime= ['Murder and nonnegligent manslaughter','Rape', 'Robbery', 'Aggravated assault']
        return self.violent_crime

    def property_crime(self):
        self.property_crime = ['Burglary','Larceny- theft', 'Motor vehicle theft']
        return self.property_crime

    def air_quality_index(self):
        self.air_quality_index = ['Days with AQI', 'Good Days', 'Moderate Days','Unhealthy for Sensitive Groups Days', 'Unhealthy Days','Very Unhealthy Days', 'Hazardous Days', 'Max AQI', '90th Percentile AQI', 'Median AQI', 'Days CO', 'Days NO2', 'Days Ozone', 'Days SO2', 'Days PM2.5', 'Days PM10']
        return self.air_quality_index

@router.post("/api/demographics_graph")
async def demographics_plot(current_city:City):
    """
    Visualize demographic information for city

    ### Query Parameters
    - city

    ### Response
    JSON string to render with react-plotly.js
    """
    city = validate_city(current_city)
    city_data = CityData(city)

    # Demographics
    city_demographics = city_data.subset[city_data.demographics()]
    city_demographics['Not Specified'] = 100 - city_demographics.sum(axis=1) # Accounting for people that did not respond
    melt = pd.melt(city_demographics)
    melt.columns = ['demographic', 'percentage']
    fig = px.pie(melt, values ='percentage', names ='demographic')
    fig.update_layout(
        title={
            'text': f'Demographics in {city}',
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig.show()

    return fig.to_json()

@router.post("/api/employment_graph")
async def employment_plot(current_city:City):
    """
    Visualize employment information for city
    - see industry breakdown and employment type

    ### Query Parameters
    - city

    ### Response
    JSON string to render with react-plotly.js
    """
    city = validate_city(current_city)
    city_data = CityData(city)

    # Industry
    industry_type = city_data.subset[city_data.industry()]
    industry_melt = pd.melt(industry_type)
    industry_melt.columns = ['industry', 'percentage']

    # Employment Type
    employment_type = city_data.subset[city_data.employment()]
    type_melt = pd.melt(employment_type)
    type_melt.columns = ['employment type', 'percentage']

    #Create subplots
    fig = make_subplots(rows=1, cols=2, subplot_titles = (f'Industry in {city}', f'Employment Types in {city}'))
    fig.add_trace(go.Bar(x = industry_melt['industry'], y = industry_melt['percentage'],
                         marker = dict(color = industry_melt['percentage'], coloraxis = "coloraxis")),
                  row = 1, col = 1)
    fig.add_trace(go.Bar(x =type_melt['employment type'], y =type_melt['percentage'],
                         marker = dict(color = type_melt['percentage'], coloraxis = "coloraxis")),
                         row = 1, col = 2)
    fig.update_layout(
        coloraxis=dict(colorscale = 'Bluered_r'),
        coloraxis_showscale = False,
        showlegend = False)

    fig.show()

    return fig.to_json()

@router.post("/api/crime_graph")
async def crime_plot(current_city:City):
    """
    Visualize crime information for city
    - see overall crime breakdown
    - visualize breakdown of violent crime and property crime

    ### Query Parameters
    - city

    ### Response
    JSON string to render with react-plotly.js
    """
    city = validate_city(current_city)
    city_data = CityData(city)

    # Crime Categories
    crime_type = city_data.subset[city_data.crime()]
    crime_melt = pd.melt(crime_type)
    crime_melt.columns = ['categories', 'total']

    # Violent Crime
    violent_crime_type = city_data.subset[city_data.violent_crime()]
    violent_crime_type_melt = pd.melt(violent_crime_type)
    violent_crime_type_melt.columns = ['violent crime type', 'total']

    # Property Crime
    property_crime_type = city_data.subset[city_data.property_crime()]
    property_crime_melt = pd.melt(property_crime_type)
    property_crime_melt.columns = ['property crime type', 'total']

    #Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles = (f"Crime Breakdown in {city}", f"Violent Crime Breakdown in {city}", f"Property Crime Breakdown in {city}"),
        specs = [[{"type":"xy", 'rowspan':2}, {"type": "pie"}],
                 [None, {"type": "pie"}]],

    )

    fig.add_trace(go.Bar(name = 'Crime Types', x = crime_melt['categories'], y = crime_melt['total']),
                  row = 1, col = 1)
    fig.add_trace(go.Pie(values = violent_crime_type_melt['total'],
                         labels = violent_crime_type_melt['violent crime type']),
                         row = 1, col = 2)
    fig.add_trace(go.Pie(values = property_crime_melt['total'],
                         labels = property_crime_melt['property crime type']),
                         row = 2, col = 2)

    fig.show()

    return fig.to_json()

@router.post("/api/aqi_graph")
async def air_quality_plot(current_city:City):
    """
    Visualize air quality information for city

    ### Query Parameters
    - city

    ### Response
    JSON string to render with react-plotly.js
    """
    city = validate_city(current_city)
    city_data = CityData(city)

    # Air Quality
    air_quality_details = city_data.subset[city_data.air_quality_index()]
    air_quality_melt = pd.melt(air_quality_details)
    air_quality_melt.columns = ['air quality indicators', 'days']
    fig = make_subplots(rows = 1, cols = 1)
    fig.add_trace(go.Bar(x = air_quality_melt['days'], y = air_quality_melt['air quality indicators'],
                         marker = dict(color = air_quality_melt['days'], coloraxis = "coloraxis"), orientation = 'h'))
    fig.update_layout(
        coloraxis=dict(colorscale = 'Viridis'),
        coloraxis_showscale = False,
        xaxis_range = [0, 360],
        title={
            'text': f'Air Quality in {city}',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig.show()

    return fig.to_json()

POPULATION_CSV = 'https://raw.githubusercontent.com/jiobu1/labspt15-cityspire-g-ds/main/notebooks/model/population2010-2019/csv/population_cleaned.csv'
FORECAST_CSV = 'https://raw.githubusercontent.com/jiobu1/labspt15-cityspire-g-ds/main/notebooks/model/population2010-2019/csv/population_prediction.csv'

@router.post('/api/population_forecast_graph')
async def population_forecast_graph(city:City):
    """
    Create visualization of historical and forecasted population

    args:
    - city: str -> The target city
    - periods: int -> number of years to forecast for

    Returns:
    Visualization of population forecast
    - 10 year of historical data
    - forecasts for number of years entered
    """

    city = validate_city(city)
    location = [city.city + ', ' + city.state]

    # Historical population data
    population = pd.read_csv(POPULATION_CSV)
    population = population[population['City,State'].isin(location)]
    population = population[['City,State', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']]
    population_melt = population.melt(id_vars=['City,State'], var_name='ds', value_name='y')
    population_melt['ds'] = (population_melt['ds']).astype(int)

    # Predictions
    forecast = pd.read_csv(FORECAST_CSV)
    predictions = forecast[forecast['City,State'].isin(location)][9:]
    predictions['year'] = (predictions['year']).astype(int)

    # Graph Data
    ax = population_melt.plot(x = 'ds', y = 'y', label='Observed', figsize= (10, 8))
    predictions[['year', 'yhat']].plot(ax = ax, x = 'year', y = 'yhat', label = "Forecast")

    # Fill to show upper and lower bounds
    # Graph predictions including the upper and lower bounds
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        name = 'Original',
        x = population_melt['ds'],
        y = population_melt['y'],
        fill = None,
        mode = 'lines',
        line_color = 'black',
        showlegend = True
    ))

    fig.add_trace(go.Scatter(
        name = 'Forecast',
        x = predictions['year'],
        y = predictions['yhat'],
        fill = None,
        mode = 'lines',
        line_color = 'red',
        showlegend = True
    ))

    fig.add_trace(go.Scatter(
        name = 'Lower Bound',
        x = predictions['year'],
        y = predictions['yhat_lower'],
        fill = None,
        mode = 'lines',
        line_color = 'gray'
    ))

    fig.add_trace(go.Scatter(
        name = 'Upper Bound',
        x = predictions['year'],
        y = predictions['yhat_upper'],
        fill='tonexty',
        mode='lines',
        line_color = 'gray'
    ))

    # Edit the layout
    fig.update_layout({
        'autosize':True,
        'title': f'{location[0]} Population Forecast',
        'title_x': 0.5,
        'xaxis_title': 'Year',
        'yaxis_title': 'Population'
        })

    fig.update_yaxes(automargin = True)
    fig.update_xaxes(automargin = True, nticks=20)

    fig.show()

    return fig.to_json()
