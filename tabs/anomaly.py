from datetime import date as dt, timedelta
import dash
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime
import json
from layouts import layout_timeseries

with open('database/country_sensors.json', 'r') as file:
    country_sens = json.load(file)

layout = html.Div([
    layout_timeseries,
    dcc.Graph(id='output-container-clustering')
], )
