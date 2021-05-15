import gzip

import dash
from dash.dependencies import Input, Output
import database
import api
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from tabs import timeseries
from tabs import worldmap
from tabs import overview
from datetime import datetime
import pandas as pd
import json

app = dash.Dash()

####################################################################
# testing purposes here ####
with open('database/2021-02-01/2021-02-01_BME280_sensor_141.json') as data_file:
    data = json.load(data_file)
df = pd.json_normalize(data, 'dataList', ['id', 'type'])
#####################################################################
with open('database/country_sensors.json', 'r') as file:
    country_sens = json.load(file)

app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.H1('Visual Analytics - Climate data'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Worldmap', value='worldmap'),
        dcc.Tab(label='Overview', value='overview'),
        dcc.Tab(label='Timeseries', value='timeseries'),
        dcc.Tab(label='Anomaly', value='anomaly')
    ]),
    html.Div(id='tabs-content-example')
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'timeseries':
        return timeseries.layout
    elif tab == 'worldmap':
        return worldmap.layout
    elif tab == 'overview':
        return worldmap.layout


# Timeseries related stuff

@app.callback(
    Output('region-id', 'options'),
    Input('land-id', 'value'))
def set_regions_options(selected_country):
    return [{'label': region, 'value': region} for region in country_sens[selected_country]]


@app.callback(
    Output('city-id', 'options'),
    Input('land-id', 'value'),
    Input('region-id', 'value'))
def set_city_options(selected_country, selected_region):
    return [{'label': city, 'value': city} for city in country_sens[selected_country][selected_region]]


@app.callback(
    Output('viable-sensor-id', 'options'),
    Input('land-id', 'value'),
    Input('region-id', 'value'),
    Input('city-id', 'value'))
def set_city_options(selected_country, selected_region, selected_city):
    return [{'label': sensorid, 'value': sensorid} for sensorid in
            country_sens[selected_country][selected_region][selected_city]]


@app.callback(
    Output('sensor_typ-dropdown', 'options'),
    Input('viable-sensor-id', 'value'))
def set_city_options(selected_id):
    if selected_id is not None:
        sensor_type = database.getSensorType(selected_id)
    return [{'label': sensor_type, 'value': sensor_type}]


@app.callback(
    Output('output-container-timeseries', 'figure'),
    Input('from_time_id', 'date'),
    Input('to_time_id', 'date'),
    Input('viable-sensor-id', 'value'),
    Input('sensor_typ-dropdown', 'value'),
    Input('type_of_measurement_id', 'value')
)
def timeseries_update(from_time, to_time, viable_sensor_id, sensor_typ, type_of_measurement):
    # always select every field, otherwise it wont react
    global df
    fig = px.line(df, x='timestamp', y='temperature')
    if viable_sensor_id is not None and type_of_measurement is not None:
        start_time = datetime.strptime(from_time, '%Y-%m-%d')
        end_time = datetime.strptime(to_time, '%Y-%m-%d')
        sensor_data = api.getSensorData(viable_sensor_id, start_time, end_time)
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
    return fig


# Worldmap
@app.callback(Output('page-2-content', 'children'), [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
