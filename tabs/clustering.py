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

# import warnings
# warnings.filterwarnings('ignore')


def clustering_logic(from_time, to_time, type_of_measurement, nr_clusters):
    sensor_types = []
    if type_of_measurement == 'temperature' or type_of_measurement == 'humidity':
        sensor_types.extend(['bme280', 'dht22', 'bmp280'])
    else:
        print("Invalid Sensor Type")
        return {}
    if nr_clusters == None:
        nr_clusters = 4

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
        raise ValueError("Calculation Error with clusters")



    fig = make_subplots(rows=nr_clusters, cols=1)
    for idx in range(0, nr_clusters):
            average_line = result[idx][0]
            df = pd.DataFrame(average_line, columns=[type_of_measurement]) # create df
            df = df.assign(Country='AVG', City='AVG', SensorID='AVG', # add other columns to df
                           Time=sensor_data[result[idx][1][0]].dataFrame[type_of_measurement].index)
            for sensor_id in result[idx][1]:
                sensor = sensor_data[sensor_id]
                sensor_df = pd.DataFrame(sensor.dataFrame[type_of_measurement], columns=[type_of_measurement]) # create df
                sensor_df = sensor_df.assign(Country=sensor.country, City=sensor.city, SensorID=sensor_id, # add other columns to df
                           Time=sensor.dataFrame[type_of_measurement].index)
                df = df.append(sensor_df, ignore_index=True) # append to big df

            fig = px.line(df, x='Time', y=type_of_measurement, color='City', facet_row='Country')


    new_height = 500 * nr_clusters
    fig.update_layout(height=new_height, title_text="text")
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
                date=(datetime.today() - timedelta(days=10)).date()
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


layout = html.Div([
    layout_clustering,
    dcc.Graph(id='output-container-clustering', style={'height': '90vh'})
], )