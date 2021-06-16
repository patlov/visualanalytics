from datetime import date as dt, timedelta
import dash
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime
import json
import api


with open('database/country_sensors.json', 'r') as file:
    country_sens = json.load(file)


def anomaly_logic(from_time, to_time, land, region, type_of_measurement):

    start_time = datetime.strptime(from_time, '%Y-%m-%d')
    end_time = datetime.strptime(to_time, '%Y-%m-%d')

    sensor_ids = api.get_sensors(country=land, state=region, return_sensors=True, type=['bme280', 'dht22', 'bmp280'])
    print("download sensors")
    sensor_data = api.download_sensors(sensor_ids, start_time, end_time)

    # TOOD: anomaly logic
    raise NotImplementedError("Anomaly not implemented yet")


    return {}

layout_anomaly = html.Div([
        html.H1("Anomaly", style={'text-align': 'center'}),
        html.P("Select the region where you want to find anomalies. You can only provide the country to search in the whole country. If country and state is provided, "
               "anomalies in the state are provided"),
        html.Label([
            "From time:",
            dcc.DatePickerSingle(
                id='from_time_id',
                min_date_allowed=datetime(2015, 8, 5),
                max_date_allowed=datetime.today() - timedelta(days=2),
                initial_visible_month=datetime.today(),
                date=(datetime.today() - timedelta(days=10)).date(),
            )
        ]),
        html.Label([
            "To time:",
            dcc.DatePickerSingle(
                id='to_time_id',
                min_date_allowed=datetime(2015, 8, 5),
                max_date_allowed=datetime.today() - timedelta(days=2),
                initial_visible_month=datetime.today(),
                date=(datetime.today() - timedelta(days=9)).date()
            ),
        ]),
        html.Br(),
        html.Label([
            "Country:",
            dcc.Dropdown(
                id='land-id',
                options=[{'label': land, 'value': land} for land in country_sens],
                value='',
                multi=False,
                className='form-select', style={'min-width': '200px'}
            ),
        ]),
        html.Label([
            "State:",
            dcc.Dropdown(id='region-id', className='form-select', style={'min-width': '200px'}),
        ]),
        html.Div([
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
                    className='form-select'
                ),
            ])
        ]),
        html.Br(),
        html.Button('Submit', id='submit', n_clicks=0, className='btn btn-primary'),
    ], style={'width': '80%', 'margin': 'auto', 'text-align': 'center'})


layout = html.Div([
    layout_anomaly,
    dcc.Graph(id='output-container-anomaly')
], )
