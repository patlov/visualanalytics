from datetime import date as dt, timedelta
import dash
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime
import json

with open('database/country_sensors.json', 'r') as file:
    country_sens = json.load(file)

layout_timeseries = html.Div([
        html.H1("Timeseries Tab", style={'text-align': 'center'}),
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
            "SensorTyp:",
            dcc.Dropdown(id='sensor_typ-dropdown'),
        ]),
        html.Label([
            "SensorID:",
            dcc.Dropdown(id='viable-sensor-id',
                         multi=True),

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
    ], style={'width': '25%'})



layout_clustering = html.Div([
        html.H1("Similarities", style={'text-align': 'center'}),
        html.P("To find similar measurement we take one sensor of each region as sample and compare it with all other regions, "
               "otherwise the clusters would be clustered by location (because close sensors will have the similar measurement"),
        html.Label([
            "From time:",
            dcc.DatePickerSingle(
                id='from_time_id',
                min_date_allowed=datetime(2015, 8, 5),
                max_date_allowed=datetime.today(),
                initial_visible_month=datetime.today(),
                date=datetime.today()
            )
        ]),
         html.Label([
            "To time:",
            dcc.DatePickerSingle(
                id='to_time_id',
                min_date_allowed=datetime(2015, 8, 5),
                max_date_allowed=datetime.today(),
                initial_visible_month=datetime.today(),
                date=datetime.today()
            ),
        ]),
        html.Br(),
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
        html.Label([
            "Number of Clusters:",
            dcc.Input(
                id="nr_clusters", type="number", placeholder=4,
                min=1, max=20, step=1
            ),
        ]),
        html.Button('Submit', id='submit', n_clicks=0),
    ], style={'width': '25%', 'margin': 'auto'})


layout_anomaly = html.Div([
        html.H1("Anomaly Tab", style={'text-align': 'center'}),
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
            "SensorTyp:",
            dcc.Dropdown(id='sensor_typ-dropdown'),
        ]),
        html.Label([
            "SensorID:",
            dcc.Dropdown(id='viable-sensor-id',
                         multi=True),

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
    ], style={'width': '25%'})
