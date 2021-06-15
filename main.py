import gzip

import dash
from dash.dependencies import Input, Output
import database
import api
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from tabs import timeseries
from tabs import worldmap
from tabs import anomaly
from tabs import clustering
from datetime import datetime
from clustering import cluster_ts
import pandas as pd
import json

app = dash.Dash(prevent_initial_callbacks=True)

with open('database/country_sensors.json', 'r') as file:
    country_sens = json.load(file)

app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.H1('Visual Analytics - Climate data'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Worldmap', value='worldmap'),
        dcc.Tab(label='Clustering', value='clustering'),
        dcc.Tab(label='Timeseries', value='timeseries'),
        dcc.Tab(label='Anomaly', value='anomaly')
    ]),
    html.Div(id='tabs-content-example')
])
app.title = 'VA Climate Data Analysis 2021'


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'timeseries':
        return timeseries.layout
    elif tab == 'clustering':
        return clustering.layout
    elif tab == 'worldmap':
        return worldmap.layout
    elif tab == 'anomaly':
        return anomaly.layout


# input related stuff
@app.callback(
    Output('region-id', 'options'),
    Input('land-id', 'value'))
def set_regions_options(selected_country):
    if selected_country in country_sens:
        return [{'label': region, 'value': region} for region in country_sens[selected_country]]
    else:
        return []


@app.callback(
    Output('city-id', 'options'),
    Input('land-id', 'value'),
    Input('region-id', 'value'))
def set_city_options(selected_country, selected_region):
    if selected_country in country_sens and selected_region in country_sens[selected_country]:
        return [{'label': city, 'value': city} for city in country_sens[selected_country][selected_region]]
    else:
        return []


@app.callback(
    Output('sensor_typ-dropdown', 'options'),
    Input('land-id', 'value'),
    Input('region-id', 'value'),
    Input('city-id', 'value'))
def set_sensors_typ_options(selected_country, selected_region, selected_city):
    if selected_country in country_sens and selected_region in country_sens[selected_country] and selected_city in country_sens[selected_country][selected_region]:
        return [{'label': sensorid, 'value': sensorid} for sensorid in country_sens[selected_country][selected_region][selected_city]]
    else:
        return []

@app.callback(
    Output('viable-sensor-id', 'options'),
    Input('land-id', 'value'),
    Input('region-id', 'value'),
    Input('city-id', 'value'),
    Input('sensor_typ-dropdown', 'value'))
def set_sensors_typ_options(selected_country, selected_region, selected_city, selected_type):
    if selected_country in country_sens \
            and selected_region in country_sens[selected_country] \
            and selected_city in country_sens[selected_country][selected_region] \
            and selected_type in country_sens[selected_country][selected_region][selected_city]:

        return [{'label': sensorid, 'value': sensorid} for sensorid in
                country_sens[selected_country][selected_region][selected_city][selected_type]]

    else:
        return []


# update on timeseries tab
@app.callback(
    Output('output-container-timeseries', 'figure'),
    Input('from_time_id', 'date'),
    Input('to_time_id', 'date'),
    Input('land-id', 'value'),
    Input('region-id', 'value'),
    Input('city-id', 'value'),
    Input('viable-sensor-id', 'value'),
    Input('sensor_typ-dropdown', 'value'),
    Input('type_of_measurement_id', 'value')
)
def timeseries_update(from_time, to_time, land, region, city, viable_sensor_id, sensor_typ, type_of_measurement):
    if viable_sensor_id is not None and type_of_measurement != '':
        start_time = datetime.strptime(from_time, '%Y-%m-%d')
        end_time = datetime.strptime(to_time, '%Y-%m-%d')
        # sensors = api.get_sensors(country=land, region=region, city=city, return_cities=True)
        sensor_data = api.download_sensors(viable_sensor_id, start_time, end_time)
        # start_time_str = start_time.strftime("%Y-%m-%d")
        # path = database.buildLocalPath(viable_sensor_id, str(sensor_typ).upper(), start_time_str)
        # if database.ZIP_MODE is False:
        #    with open(path, 'r', encoding='utf8', errors='ignore') as sensor_file:
        #        sens_data = json.load(sensor_file)
        #else:
        #    with gzip.open(path, 'r') as fin:
        #        sens_data = json.loads(fin.read().decode('utf-8'))
        # df = pd.json_normalize(sensor_data[viable_sensor_id], 'dataList', ['id', 'type'])

        fig = make_subplots(rows=len(sensor_data), cols=1)
        for idx in range(0, len(sensor_data)):
            fig.add_trace(go.Line(x=sensor_data[viable_sensor_id[idx]].dataFrame.index,
                                  y=sensor_data[viable_sensor_id[idx]].dataFrame[type_of_measurement],
                                  name=(str(viable_sensor_id[idx]))), row=(idx+1), col=1)
        return fig
    return {}


# Worldmap
@app.callback(Output('page-2-content', 'children'), [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)

# update on clustering tab
@app.callback(
    Output('output-container-clustering', 'figure'),
    Input('from_time_id', 'date'),
    Input('to_time_id', 'date'),
    Input('type_of_measurement_id', 'value'),
    Input('nr_clusters', 'value'),
    Input('submit', 'n_clicks')
)
def clustering_update(from_time, to_time, type_of_measurement, nr_clusters, submit):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'submit' not in changed_id: # check if button was clicked
        return {}
    print("yes we clicked submit - lets go")
    # submit button clicked
    if type_of_measurement == None:
        return {}

    if nr_clusters == None:
        nr_clusters = 4
    sensor_types = []
    if type_of_measurement == 'temperature' or type_of_measurement == 'humidity':
        sensor_types.extend(['bme280', 'dht22', 'bmp280'])
    else:
        print("Invalid Sensor Type")
        raise ValueError(type_of_measurement + " is a invalid type")
        return {}

    start_time = datetime.strptime(from_time, '%Y-%m-%d')
    end_time = datetime.strptime(to_time, '%Y-%m-%d')

    sensor_ids = api.get_sensors(return_sensors=True, num_sensors=1, type=['bme280', 'dht22', 'bmp280'])
    sensor_data = api.download_sensors(sensor_ids, start_time, end_time)
    sensor_ids = [*sensor_data]
    MAX_TEMP = 50
    MIN_TEMP = -50
    result = cluster_ts(sensor_data, type_of_measurement, nr_clusters, MIN_TEMP, MAX_TEMP)

    df = px.data.gapminder().query("country=='Canada'")
    df = px.data.stocks()
    assert len(result) == nr_clusters
    fig = make_subplots(rows=nr_clusters, cols=1)
    for idx in range(0, nr_clusters):
        try:
            average_line = result[idx][0]
            # fig.add_trace(go.Line(x=average_line, y=sensor_data[result[idx][1][0]].dataFrame[type_of_measurement].index, name="AVERAGE"), row=(idx+1), col=1)
            # fig.add_trace(px.line(result, x="year", y="lf", title="title"))
            for sensor in result[idx][1]:
                series = sensor_data[sensor].dataFrame[type_of_measurement]
                time_series = sensor_data[sensor].dataFrame[type_of_measurement].index
                fig.add_trace(go.Line(x=time_series, y=series, name=str(sensor)), row=(idx+1), col=1)
        except KeyError:
            continue
    new_height = 500 * nr_clusters
    fig.update_layout(height=new_height, title_text="text")
    return fig


# update on anomaly tab
@app.callback(
    Output('output-container-anomaly', 'figure'),
    Input('from_time_id', 'date'),
    Input('to_time_id', 'date'),
    Input('viable-sensor-id', 'value'),
    Input('sensor_typ-dropdown', 'value'),
    Input('type_of_measurement_id', 'value')
)
def anomaly_update(from_time, to_time, viable_sensor_id, sensor_typ, type_of_measurement):
    if viable_sensor_id is not None and type_of_measurement is not None:
        start_time = datetime.strptime(from_time, '%Y-%m-%d')
        end_time = datetime.strptime(to_time, '%Y-%m-%d')
        sensor_data = api.download_sensors(viable_sensor_id, start_time, end_time)
        start_time_str = start_time.strftime("%Y-%m-%d")
        path = database.buildLocalPath(viable_sensor_id, str(sensor_typ).upper(), start_time_str)

        if database.ZIP_MODE is False:
            with open(path, 'r', encoding='utf8', errors='ignore') as sensor_file:
                sens_data = json.load(sensor_file)
        else:
            with gzip.open(path, 'r') as fin:
                sens_data = json.loads(fin.read().decode('utf-8'))

        df = pd.json_normalize(sens_data, 'dataList', ['id', 'type'])
        fig1 = px.line(df, x='timestamp', y=type_of_measurement)
        return fig1
    return {}

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
