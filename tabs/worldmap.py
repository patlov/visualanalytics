import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import api as api
import plotly.express as px

absolute_path = "/home/pat/Desktop/University/Master/2_semester/visualanalytics"

token = open("keys/mapbox_token").read()
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

sensors = api.get_sensors(return_sensorids=True, num_sensors=1)
print("x")


fig = px.density_mapbox(us_cities, lat="lat", lon="lon", z='Population', zoom=2, height=850)
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
