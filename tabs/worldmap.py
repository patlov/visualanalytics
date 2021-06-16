import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import api as api
import plotly.express as px
import json
import aiohttp
import asyncio


# async way to get fast all sensors
# async def get(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             sensor_data = await response.read()
#             sensor_json = json.loads(sensor_data)
#             if len(sensor_json) > 0:
#                 return sensor_json[0]
#
#
# token = open("keys/mapbox_token").read()
# sensor_per_city = api.get_sensors(return_sensors=True, num_sensors=1, type=['bme280', 'dht22', 'bmp280'])
#
# loop = asyncio.get_event_loop()
# all_sensors = [get("https://data.sensor.community/airrohr/v1/sensor/" + sens_id + '/') for sens_id in sensor_per_city]
# results = loop.run_until_complete(asyncio.gather(*all_sensors))
#
# # remove none types
# results = [i for i in results if i]
#
# # adjust and create normalized dataframe out of the json list
# sensor_df = pd.json_normalize(results, record_path='sensordatavalues', meta=['timestamp', 'location'])
# sensor_loc = pd.json_normalize(sensor_df['location'], meta=['latitude', 'longitude'])
# sensor_df['latitude'] = sensor_loc['latitude'].astype(float)
# sensor_df['longitude'] = sensor_loc['longitude'].astype(float)
#
# fig = px.density_mapbox(sensor_df, hover_name='value_type', lat="latitude", lon="longitude", z='value', zoom=2,
#                         height=850)
# fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
# fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# fig.update_layout(
#     mapbox_style="white-bg",
#     mapbox_layers=[
#         {
#             "below": 'traces',
#             "sourcetype": "raster",
#             "sourceattribution": "United States Geological Survey",
#             "source": [
#                 "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
#             ]
#         }
#     ])

layout = html.Div([
    dcc.Graph(
        id='example-graph-2',
        figure=None
    ),
    html.Div(id='page-2-content')
])
