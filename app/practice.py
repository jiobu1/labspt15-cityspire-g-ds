
from pickle import load
import requests
from bs4 import BeautifulSoup as bs
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
from fbprophet import Prophet
from pypika import Query, Table, CustomFunction
import asyncio
from app.db import database, select, select_all
from typing import List, Optional
from app.ml import City, validate_city
from app.data.files.state_abbr import us_state_abbrev as abbr

router = APIRouter()

@router.post('/api/population_forecast')
def population_forecast(city:City, periods=10):
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

    # Load Dataset
    population = pd.read_csv('https://raw.githubusercontent.com/jiobu1/labspt15-cityspire-g-ds/main/notebooks/model/population2010-2019/csv/population_cleaned.csv')
    population.reset_index(level=0, inplace=True)

    # Melt table into ds and y
    population_melt = population[['City,State', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']]
    population_melt = population_melt.melt(id_vars=['City,State'], var_name='ds', value_name='y')

    # Isolate city data
    location = city.city + ', ' + city.state
    print(location)
    df_ = population_melt[population_melt['City,State'] == location][['ds','y']]
    print(df_)
    df_.columns = ['ds','y']


    # Fit and Predict on city dataframe
    # Model
    m = Prophet(interval_width=0.95)
    # Fit model
    m.fit(df_)
    print('I AM HERE!!!!')
    future = m.make_future_dataframe(periods=periods, freq='Y')
    print('NOW I AM HERE!!!!')
    # Predict
    forecast = m.predict(future)
    print('THIRD I AM HERE!!!!')

    predictions = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']][9:]
    predictions['ds'] = pd.DatetimeIndex(predictions['ds']).year
    predictions[['yhat', 'yhat_lower', 'yhat_upper']] =  predictions[['yhat', 'yhat_lower', 'yhat_upper']].round()

    # Create graph
    # Graph first 10 years
    df_['ds'] = df_['ds'].astype(int)
    predictions['ds'] = predictions['ds'].astype(int)

    # Graph historical data
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        name = 'Original',
        x = list(df_['ds']),
        y = list(df_['y']),
        fill = None,
        mode = 'lines',
        line_color = 'black',
        showlegend = True
    ))

    # Graph predictions including the upper and lower bounds
    fig.add_trace(go.Scatter(
        name = 'Forecast',
        x = list(predictions['ds']),
        y = list(predictions['yhat']),
        fill = None,
        mode = 'lines',
        line_color = 'red',
        showlegend = True
    ))

    fig.add_trace(go.Scatter(
        name = 'Lower Bound',
        x = list(predictions['ds']),
        y = list(predictions['yhat_lower']),
        fill = None,
        mode = 'lines',
        line_color = 'gray',
    ))

    fig.add_trace(go.Scatter(
        name = 'Upper Bound',
        x = list(predictions['ds']),
        y = list(predictions['yhat_upper']),
        fill='tonexty',
        mode='lines',
        line_color = 'gray',
    ))

    # Edit the layout
    fig.update_layout({
        'autosize':True,
        'title': f'{city[0]} Population Forecast',
        'title_x': 0.5,
        'xaxis_title': 'Year',
        'yaxis_title': 'Population'
        })

    fig.update_yaxes(automargin = True,)
    fig.update_xaxes(automargin = True, nticks=20)

    fig.show()

    return fig.to_json