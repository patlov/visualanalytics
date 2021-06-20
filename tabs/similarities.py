import dash_core_components as dcc
import dash_html_components as html
from datetime import date as dt, timedelta
import dash
from datetime import datetime
import pandas as pd
import json
from clustering import cluster_ts
import plotly.express as px
from dash.dependencies import Input, Output
import database
import api
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from tabs import timeseries
from tabs import worldmap
from tabs import anomaly
from tabs import similarities
import dash_bootstrap_components as dbc

# import warnings
# warnings.filterwarnings('ignore')
with open('database/country_sensors.json', 'r', encoding='utf-8') as file:
    country_sens = json.load(file)


def find_time_series(average, cluster_result_sensors, sensor_data, type_of_measurement):
    for i in range(len(cluster_result_sensors)):
        time_series = sensor_data[cluster_result_sensors[i]].dataFrame[type_of_measurement].index
        if len(time_series) == len(average):
            return time_series
    raise ValueError("No time series with same length found")

def similarities_logic(from_time, to_time, country, state, nr_sensors, type_of_measurement, nr_clusters):

    start_time = datetime.strptime(from_time, '%Y-%m-%d')
    end_time = datetime.strptime(to_time, '%Y-%m-%d')

    if country == '':
        country = None
    if state == '':
        state = None

    sensor_ids = api.get_sensors(country=country, state=state, return_sensors=True, num_sensors=nr_sensors, type=['bme280', 'dht22', 'bmp280'])
    print("download sensors")
    sensor_data = api.download_sensors(sensor_ids, start_time, end_time)
    MAX_TEMP = 50
    MIN_TEMP = -50
    print("clustering sensors")
    result = list(reversed(cluster_ts(sensor_data, type_of_measurement, nr_clusters, MIN_TEMP, MAX_TEMP)))

    if len(result) != nr_clusters:
        print(result)
        raise ValueError("Calculation Error with clusters")

    db_index = []

    df = pd.DataFrame()
    for idx in range(nr_clusters):
            db_index.append(result[idx][0])
            c = result[idx][1]
            average_line = c['centroid']
            sensor_list = c['sensor_ids']
            time_series = find_time_series(average_line, sensor_list, sensor_data, type_of_measurement)
            df_avg = pd.DataFrame(average_line, columns=[type_of_measurement]) # create df vor average
            df_avg = df_avg.assign(ClusterID=idx+1, Country='AVERAGE', City='AVERAGE', SensorID='AVERAGE', # add other columns to df average
                           Time=time_series)
            df = df.append(df_avg, ignore_index=True) # add it to big df
            for sensor_id in sensor_list:
                sensor = sensor_data[sensor_id]
                sensor_df = pd.DataFrame(sensor.dataFrame[type_of_measurement], columns=[type_of_measurement]) # create df
                sensor_df = sensor_df.assign(ClusterID=idx+1, Country=sensor.country, City=sensor.city, SensorID=sensor_id, # add other columns to df
                           Time=sensor.dataFrame[type_of_measurement].index)
                df = df.append(sensor_df, ignore_index=True) # append to big df

    coloring = 'Country'
    if country != None:
        coloring = 'City'
    if state != None:
        coloring = 'SensorID'
    fig = px.line(df, x='Time', y=type_of_measurement, color=coloring, hover_name='City', line_group='City', facet_row='ClusterID')

    fig.update_traces(patch={"line":{"color":"red", "width":4}},
                  selector={"legendgroup":"AVERAGE"})

    new_height = 500 * nr_clusters
    fig.update_layout(height=new_height)

    return_dict = {
        'fig' : fig,
        'db_indices' : db_index, # db index of anomaly
        'nr_sensors' : len(sensor_data)
        }
    return return_dict


left_form = html.Div([
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
        html.Br(),
        html.Div([
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
                    style={'margin' : '1em', 'min-width': '200px'}
                ),
            ], className='text-primary', style={'font-weight': 'bold'})
        ]),
        html.Br(),
        html.Label([
            "Country:",
            dcc.Dropdown(
                id='land-id',
                options=[{'label': land, 'value': land} for land in country_sens],
                value='',
                multi=False,
                className='form-select', style={'min-width': '200px', 'margin' : '0 1em 0 1em'}
            ),
        ]),
        html.Label([
            "State:",
            dcc.Dropdown(id='region-id', value='', className='form-select', style={'min-width': '200px'}),
        ]),
        html.Label([
        "Number of Sensors per Region: (default 1)",
        dcc.Slider(
            id="nr_sensors", value=1,
            min=1, max=50, step=1, className='form-range',
            marks={
                1: {'label': '1', 'style': {'color': '#77b0b1'}},
                10: {'label': '10'},
                20: {'label': '20'},
                30: {'label': '30'},
                40: {'label': '40'},
                50: {'label': '50', 'style': {'color': '#f50'}}
            },
        ),
        html.Div(id='nr_sensors-output-container')
        ]),
        html.Br(),
        html.Label([
            "Number of Clusters: (default 4)",
            dcc.Slider(
                id="nr_clusters", value=4,
                min=1, max=20, step=1,
                marks={
                    1: {'label': '1', 'style': {'color': '#77b0b1'}},
                    10: {'label': '10'},
                    20: {'label': '20'},
                    30: {'label': '30'},
                    40: {'label': '40'},
                    50: {'label': '50', 'style': {'color': '#f50'}}
                },
            ),
            html.Div(id='slider-output-container')
        ]),
        html.Br(),
        html.Button('Submit', id='submit', n_clicks=0, className='btn btn-primary'),
])

right_form = html.Div([
    html.H2("Cluster Details"),
    html.Div(id='similarities-overview-output-container'),
    html.H4("DB Index"),
    html.Div(id='similarities-detail-output-container')
])

layout_similarities = html.Div([
        html.H1("Similarities", style={'text-align': 'center', 'margin-top':'1em'}),
        html.P("To find similar measurement we take one sensor of each region as sample and compare it with all other regions, "
               "otherwise the clusters would be clustered by location (because close sensors will have the similar measurement"),
        dbc.Row(
            [
                dbc.Col(left_form, width=4, style={'background': '#e6f9ff', 'padding': '1em', 'margin':'1em'}),
                dbc.Col(right_form, width=4, style={'background': '#e6ffcc', 'padding': '1em', 'margin':'1em'}),
            ],
            justify="center",
        ),
    ], style={'width': '80%', 'margin': 'auto', 'text-align':'center'})


layout = html.Div([
    layout_similarities,
    dcc.Loading(children=[dcc.Graph(id='output-container-similarities', style={'height': '90vh'})], color='#ff5c33', type='graph'),
], )