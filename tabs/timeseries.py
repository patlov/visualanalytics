from datetime import date
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import calendar
import json

# data = pd.read_json('2021-02-01_BME280_sensor_141.json')
# print(df['dataList'])

with open('2021-02-01_BME280_sensor_141.json') as data_file:
    data = json.load(data_file)

df = pd.json_normalize(data, 'dataList', ['id', 'type'])

# fig = go.Figure([go.Scatter(x=df['timestamp'], y=df['temperature'])])


year_list = range(2000, datetime.today().year + 1)
month_list = range(1, 13)

layout = html.Div([
    # html.Label('Multi-Select Dropdown'),
    html.Div([
        dcc.RangeSlider(
            id='year--slider',
            min=year_list[0],
            max=year_list[-1],
            value=[year_list[0], year_list[-1]],
            marks={'2000': '2000', '2010': '2010', '2021': '2021'},
            allowCross=False
        ),
        dcc.RangeSlider(
            id='month--slider',
            min=month_list[0],
            max=month_list[-1],
            marks={month_nr: {'label': calendar.month_name[month_nr]} for month_nr in month_list},
            value=[month_list[0], month_list[-1]],
            allowCross=False
        ),
    ], style={'width': '40%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Sensor-Type'),
        dcc.Dropdown(
            id='sensor_typ-dropdown',
            options=[
                {'label': 'Temperature', 'value': 'temperature'},
                {'label': 'Humidity', 'value': 'humidity'},
                {'label': 'Pressure', 'value': 'pressure'}
            ],
            value='temperature',
            multi=False
        ),
    ], style={'width': '25%'}),
    dcc.Graph(id='output-container-timeseries')
], )
