from datetime import date as dt, timedelta
import dash
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime
import json

with open('database/country_sensors.json', 'r') as file:
    country_sens = json.load(file)

layout = html.Div([

    #html.Div([
    #    dcc.Input(
    #        id='steps_interval',
    #        type='number'
    #    )
    #], style={'width': '25%'}),
    html.Div([
        # html.Label('Sensor-Type'),
        html.Label([
            "From time:",
            dcc.DatePickerSingle(
                id='from_time_id',
                min_date_allowed=datetime(1995, 8, 5),
                max_date_allowed=datetime.today(),
                initial_visible_month=datetime.today(),
                date=datetime.today()
            )
        ]),
         html.Label([
            "To time:",
            dcc.DatePickerSingle(
                id='to_time_id',
                min_date_allowed=datetime(1995, 8, 5),
                max_date_allowed=datetime.today(),
                initial_visible_month=datetime.today(),
                date=datetime.today()
            ),
        ]),
        html.Br(),
        html.Label([
            "Land:",
            dcc.Dropdown(
                id='land-id',
                options=[{'label': land, 'value': land} for land in country_sens],
                value='',
                multi=False
            ),
        ]),
        html.Label([
            "Region:",
            dcc.Dropdown(id='region-id'),
        ]),
        html.Label([
            "City:",
            dcc.Dropdown(id='city-id'),
        ]),
        html.Label([
            "SensorID:",
            dcc.Dropdown(id='viable-sensor-id'),
        ]),
        html.Label([
            "SensorTyp:",
            dcc.Dropdown(id='sensor_typ-dropdown'),
        ]),
        html.Label([
            "Type of Measurement:",
            dcc.Dropdown(
                id='type_of_measurement_id',
                options=[
                    {'label': 'Temperature', 'value': 'temperature'},
                    {'label': 'Humidity', 'value': 'humidity'},
                ],
                value='',
                multi=False
            ),
        ]),
    ], style={'width': '25%'}),
    dcc.Graph(id='output-container-timeseries')
], )
