import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import api as api
import plotly.express as px
import urllib.request, json

token = open("keys/mapbox_token").read()
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

with urllib.request.urlopen("https://data.sensor.community/static/v2/data.json") as url:
    sensor_json = json.loads(url.read().decode())

sensor_norm = pd.json_normalize(sensor_json, record_path='sensordatavalues', meta=['timestamp', 'location'])
sensor_loc = pd.json_normalize(sensor_norm['location'], meta=['latitude', 'longitude'])
sensor_norm['latitude'] = sensor_loc['latitude'].astype(float)
sensor_norm['longitude'] = sensor_loc['longitude'].astype(float)

fig = px.density_mapbox(sensor_norm, lat="latitude", lon="longitude", z='value', zoom=2, height=850)
fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])

layout = html.Div([
    dcc.Graph(
        id='example-graph-2',
        figure=fig
    ),
    html.Div(id='page-2-content')
])
