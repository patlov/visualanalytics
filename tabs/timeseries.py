from datetime import date as dt, timedelta
import dash
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime
import json
import dash_bootstrap_components as dbc

with open('database/country_sensors.json', 'r', encoding='utf-8') as file:
    country_sens = json.load(file)

styles = {
    'input_fields': {
        'min-width': '200px',
        'display': 'block'
    }
}

layout_timeseries = html.Div([
        html.H1("Timeseries", style={'text-align': 'center', 'margin-top':'1em'}),
        html.P(
        "You can specifiy which sensor in which time range should be displayed"),
    html.Label([
        "From time:",
        dcc.DatePickerSingle(
            id='from_time_id',
            min_date_allowed=datetime(2015, 8, 5),
            max_date_allowed=datetime.today() - timedelta(days=2),
            initial_visible_month=datetime.today(),
            date=(datetime.today() - timedelta(days=1)).date()
        )
    ]),
    html.Label([
        "To time:",
        dcc.DatePickerSingle(
            id='to_time_id',
            min_date_allowed=datetime(2015, 8, 5),
            max_date_allowed=datetime.today() - timedelta(days=2),
            initial_visible_month=datetime.today(),
            date=(datetime.today()).date()
        ),
    ]),
    html.Br(),
    html.Label([
        "Land:",
        dcc.Dropdown(
            id='land-id',
            options=[{'label': land, 'value': land} for land in country_sens],
            value='',
            multi=False,
            className='form-select',
            style=styles['input_fields']
        ),
    ], id='land_label_id'),
    html.Br(),
    html.Label([
        "Region:",
        dcc.Dropdown(id='region-id', className='form-select',  style=styles['input_fields']),
    ], id='region_label_id'),
    html.Br(),
    html.Label([
        "City:",
        dcc.Dropdown(id='city-id', className='form-select',  style=styles['input_fields']),
    ], id='city_label_id'),
    html.Br(),
    html.Label([
        "SensorTyp:",
        dcc.Dropdown(id='sensor_typ-dropdown', className='form-select',  style=styles['input_fields']),
    ], id='sensortyp_label_id'),
    html.Br(),
    html.Label([
        "SensorID:",
        dcc.Dropdown(id='viable-sensor-id',
                     multi=True,
                     className='form-select',
                     style=styles['input_fields']
                     )
    ], id='sensorID_label_id'),
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
            multi=False,
            className='form-select',
            style=styles['input_fields']
        ),
    ], id='type_of_measurement_label_id'),
    html.Br(),
    html.Button('Submit', id='submit', n_clicks=0, className='btn btn-primary')
], style={'width': '80%', 'margin': 'auto', 'text-align': 'center'})

layout = html.Div([
    layout_timeseries,
    dcc.Loading(children=[dcc.Graph(id='output-container-timeseries', style={'height': '90vh'})], color='#ff5c33',
                type='graph'),
], )
