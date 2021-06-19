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
from tabs import clustering
import dash_bootstrap_components as dbc

# import warnings
# warnings.filterwarnings('ignore')



def find_time_series(average, cluster_result_sensors, sensor_data, type_of_measurement):
    for i in range(len(cluster_result_sensors)):
        time_series = sensor_data[cluster_result_sensors[i]].dataFrame[type_of_measurement].index
        if len(time_series) == len(average):
            return time_series
    raise ValueError("No time series with same length found")

def clustering_logic(from_time, to_time, type_of_measurement, nr_clusters):

    start_time = datetime.strptime(from_time, '%Y-%m-%d')
    end_time = datetime.strptime(to_time, '%Y-%m-%d')

    sensor_ids = api.get_sensors(return_sensors=True, num_sensors=1, type=['bme280', 'dht22', 'bmp280'])
    print("download sensors")
    sensor_data = api.download_sensors(sensor_ids, start_time, end_time)
    MAX_TEMP = 50
    MIN_TEMP = -50
    print("clustering sensors")
    result = cluster_ts(sensor_data, type_of_measurement, nr_clusters, MIN_TEMP, MAX_TEMP)

    if len(result) != nr_clusters:
        print(result)
        raise ValueError("Calculation Error with clusters")

    df = pd.DataFrame()
    for idx in range(nr_clusters):
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

    fig = px.line(df, x='Time', y=type_of_measurement, color='Country', hover_name='City', line_group='City', facet_row='ClusterID')

    fig.update_traces(patch={"line":{"color":"red", "width":4}},
                  selector={"legendgroup":"AVERAGE"})

    new_height = 500 * nr_clusters
    fig.update_layout(height=new_height)
    return fig

layout_clustering = html.Div([
        html.H1("Similarities", style={'text-align': 'center'}),
        html.P("To find similar measurement we take one sensor of each region as sample and compare it with all other regions, "
               "otherwise the clusters would be clustered by location (because close sensors will have the similar measurement"),
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
        html.Label([
            "Number of Clusters:",
            dcc.Input(
                id="nr_clusters", type="range", value=4,
                min=1, max=20, step=1, className='form-range'
            ),
            html.Div(id='slider-output-container')
        ]),
        html.Br(),
        html.Button('Submit', id='submit', n_clicks=0, className='btn btn-primary'),
    ], style={'width': '80%', 'margin': 'auto', 'text-align':'center'})


layout = html.Div([
    layout_clustering,
    dcc.Loading(children=[dcc.Graph(id='output-container-clustering', style={'height': '90vh'})], color='#ff5c33', type='graph'),
], )