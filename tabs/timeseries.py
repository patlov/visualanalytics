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
        'min-width': '150px',
        'margin': '1em'
    }
}

layout_timeseries = html.Div([
    html.H1("Timeseries", style={'text-align': 'center', 'margin-top': '1em'}),
    html.P(
        "You can specifiy which sensor in which time range should be displayed"),
    html.Label([
        "From time:*",
        dcc.DatePickerSingle(
            id='from_time_id',
            min_date_allowed=datetime(2015, 8, 5),
            max_date_allowed=datetime.today() - timedelta(days=2),
            initial_visible_month=datetime.today(),
            date=(datetime.today() - timedelta(days=10)).date(),
            style={'margin' : '1em'}
        )
    ], className='text-primary', style={'font-weight': 'bold'}),
    html.Label([
        "To time:*",
        dcc.DatePickerSingle(
            id='to_time_id',
            min_date_allowed=datetime(2015, 8, 5),
            max_date_allowed=datetime.today() - timedelta(days=2),
            initial_visible_month=datetime.today(),
            date=(datetime.today() - timedelta(days=9)).date(),
            style={'margin' : '1em'}
        ),
    ], className='text-primary', style={'font-weight': 'bold'}),
    dbc.Row(
        [
            dbc.Col(
                html.Label([
                    "Country:*",
                    dcc.Dropdown(
                        id='land-id',
                        options=[{'label': land, 'value': land} for land in country_sens],
                        value='',
                        multi=False,
                        className='form-select',
                        style=styles['input_fields']
                    ),
                ], id='land_label_id', className='text-primary', style={'font-weight': 'bold'})
            ),
            dbc.Col(
                html.Label([
                    "State:*",
                    dcc.Dropdown(id='region-id', className='form-select', style=styles['input_fields']),
                ], id='region_label_id', className='text-primary', style={'font-weight': 'bold'}),
            ),
            dbc.Col(
                html.Label([
                    "City:*",
                    dcc.Dropdown(id='city-id', className='form-select', style=styles['input_fields']),
                ], id='city_label_id', className='text-primary', style={'font-weight': 'bold'}),
            ),
            dbc.Col(
                html.Label([
                    "Sensor type:*",
                    dcc.Dropdown(id='sensor_typ-dropdown', className='form-select', style=styles['input_fields']),
                ], id='sensortyp_label_id', className='text-primary', style={'font-weight': 'bold'}),
            ),
            dbc.Col(
                html.Label([
                    "Sensor ID:*",
                    dcc.Dropdown(id='viable-sensor-id',
                                 multi=True,
                                 className='form-select',
                                 style=styles['input_fields']
                                 )
                ], id='sensorID_label_id', className='text-primary', style={'font-weight': 'bold'}),
            ),
            dbc.Col(
                html.Label([
                    "Type of Measurement:*",
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
                ], id='type_of_measurement_label_id', className='text-primary', style={'font-weight': 'bold'}),
            ),
            dbc.Col(
                    dbc.Checklist(
                        options=[
                            {"label": "3D visualisation (temperature and humidity", "value": 1},
                        ],
                        value='',
                        id="3d_switcher",
                        inline=True,
                        switch=True,
                        style={'margin' : '1em'}
                    ),
            )
        ],
        justify="center",
    ),
    html.Button('Submit', id='submit', n_clicks=0, className='btn btn-primary')
])

info_ts = html.Div([
    html.H1("Timeseries Instruction", style={'text-align': 'center', 'margin-top': '1em'}),
    html.Label([
        "Please choose an appropriate sensor, by selecting beforehand it either by clicking on the worldmap or clicking",
        "the land,"
        "the region,"
        "the city,"
        "sensor_type,"
        "sensorID,"
        "type of measurement."
    ])
])


layout_ts = html.Div([
    dbc.Row(
        [
            dbc.Col(layout_timeseries, width=4, style={'background': '#e6f9ff', 'padding': '1em', 'margin': '1em'}),
            dbc.Col(info_ts, width=4, style={'background': '#e6ffcc', 'padding': '1em', 'margin': '1em'}),
        ],
        justify="center",
    ),
], style={'width': '80%', 'margin': 'auto', 'text-align': 'center'})

layout = html.Div([
    layout_ts,
    dcc.Loading(children=[dcc.Graph(id='output-container-timeseries', style={'height': '90vh'})], color='#ff5c33',
                type='graph'),
], )
