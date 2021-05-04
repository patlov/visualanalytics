import dash
from dash.dependencies import Input, Output
import database
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from tabs import timeseries
from tabs import worldmap
from tabs import overview
import pandas as pd
import json
from datetime import *
####################################################################
# testing purposes here ####
with open('testData/2021-02-01_BME280_sensor_141.json') as data_file:
    data = json.load(data_file)
df = pd.json_normalize(data, 'dataList', ['id', 'type'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values(["timestamp"])
df['temperature'] = pd.to_numeric(df['temperature'], downcast='float')
df['humidity'] = pd.to_numeric(df['humidity'], downcast='float')
df['pressure'] = pd.to_numeric(df['pressure'], downcast='float')
#####################################################################
app = dash.Dash()

app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.H1('Visual Analytics - Climate data'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Worldmap', value='worldmap'),
        dcc.Tab(label='Overview', value='overview'),
        dcc.Tab(label='Timeseries', value='timeseries'),
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


# Timeseries
@app.callback(Output('output-container-timeseries', 'figure'),
              Input('year--slider', 'value'),
              Input('month--slider', 'value'),
              Input('sensor_typ-dropdown', 'value'))
def timeseries_update(year, month, sensor_typ):
    print(df[sensor_typ])
    print(year[0])
    print(month[0])
    fig = px.line(df, x='timestamp', y=sensor_typ, range_x=['2021-' + str(month[0]) + '-01',
                                                            '2021-' + str(month[1]) + '-30'])
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
