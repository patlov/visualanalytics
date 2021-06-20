from datetime import date as dt, timedelta
import dash
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime
import json
import api
from clustering import cluster_ts
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

with open('database/country_sensors.json', 'r', encoding='utf-8') as file:
    country_sens = json.load(file)

def find_time_series(average, cluster_result_sensors, sensor_data, type_of_measurement):
    for i in range(len(cluster_result_sensors)):
        time_series = sensor_data[cluster_result_sensors[i]].dataFrame[type_of_measurement].index
        if len(time_series) == len(average):
            return time_series
    raise ValueError("No time series with same length found")

def anomaly_logic(from_time, to_time,country, state, type_of_measurement):

    start_time = datetime.strptime(from_time, '%Y-%m-%d')
    end_time = datetime.strptime(to_time, '%Y-%m-%d')

    if country == '':
        country = None
    if state == '':
        state = None

    nr_sensors = 1
    if country != None:
        nr_sensors = 10
    if state != None:
        nr_sensors = 50

    sensor_ids = api.get_sensors(country=country, state=state, return_sensors=True, num_sensors=nr_sensors, type=['bme280', 'dht22', 'bmp280'])
    print("download sensors")
    sensor_data = api.download_sensors(sensor_ids, start_time, end_time)
    MAX_TEMP = 80
    MIN_TEMP = -80
    nr_clusters = 5

    result = list(cluster_ts(sensor_data, type_of_measurement, nr_clusters, MIN_TEMP, MAX_TEMP))

    if len(result) != nr_clusters:
        print(result)
        raise ValueError("Calculation Error with clusters")

    df = pd.DataFrame()
    for idx in range(nr_clusters):

        sensor_list = result[idx][1]['sensor_ids']
        for sensor_id in sensor_list:
            sensor = sensor_data[sensor_id]
            sensor_df = pd.DataFrame(sensor.dataFrame[type_of_measurement], columns=[type_of_measurement]) # create df
            if idx == 0:
                sensor_df = sensor_df.assign(ClusterID=1, Country=sensor.country, City=sensor.city, SensorID=sensor_id, # add other columns to df
                           Time=sensor.dataFrame[type_of_measurement].index)
            else:
                sensor_df = sensor_df.assign(ClusterID=2, Country=sensor.country, City=sensor.city, SensorID=sensor_id, # add other columns to df
                           Time=sensor.dataFrame[type_of_measurement].index)
            df = df.append(sensor_df, ignore_index=True) # append to big df

    coloring = 'Country'
    if country != None:
        coloring = 'City'
    if state != None:
        coloring = 'SensorID'
    fig = px.line(df, x='Time', y=type_of_measurement, color=coloring, hover_name='City', line_group='City', facet_row='ClusterID')

    new_height = 500 * 2 # because we only have 2 clusters in the end
    fig.update_layout(height=new_height)
    return_dict = {
        'fig' : fig,
        'db_index' : result[0][0], # db index of anomaly
        'nr_sensors' : len(sensor_data)
        }
    return return_dict


left_form = html.Div([
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
            dcc.Dropdown(id='region-id', value='', className='form-select', style={'min-width': '200px'}),
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
])

right_form = html.Div([
    html.H2("Anomaly Details"),
    html.Div(id='anomaly-overview-output-container', style={'text-align':'left', 'padding-left':'2em'}),
    html.H4("DB Index"),
    html.Div(id='anomaly-detail-output-container')
])

layout_anomaly = html.Div([
        html.H1("Anomaly", style={'text-align': 'center', 'margin-top':'1em'}),
        html.P("Select the region where you want to find anomalies. You can only provide the country to search in the whole country. If country and state is provided, "
               "anomalies in the state are provided"),
        dbc.Row(
            [
                dbc.Col(left_form, width=4, style={'background': '#e6f9ff', 'padding': '1em', 'margin': '1em'}),
                dbc.Col(right_form, width=4, style={'background': '#e6ffcc', 'padding': '1em', 'margin': '1em'}),
            ],
            justify="center",
        ),

    ], style={'width': '80%', 'margin': 'auto', 'text-align': 'center'})


layout = html.Div([
    layout_anomaly,
    dcc.Loading(children=[dcc.Graph(id='output-container-anomaly')], color='#ff5c33', type='graph'),
], )
