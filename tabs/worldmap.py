import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import api as api
import plotly.express as px
import json
import aiohttp
import asyncio
import dash_bootstrap_components as dbc

# workaround, because of sensor HTTP configuration
# limit amount of parallel connections
# connector = aiohttp.TCPConnector(limit=50)

# kill keep alive
# connector = aiohttp.TCPConnector(force_close=True)

# sensor_per_city = api.get_sensors(return_sensors=True, num_sensors=1, type=['bme280', 'dht22', 'bmp280'])
sensor_per_country = api.get_state_sensors(num_cities=1, type=['bmp280', 'dht22', 'bmp280'])
token = open("keys/mapbox_token").read()

sensors_from_web = None
sensor_df = None


def emptyMap():
    fig = go.Figure()
    fig.update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[
            {
                "text": "Please select type of value",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                    "size": 24
                }
            }
        ]
    )
    return fig


# async way to get fast all sensors
async def get(url):
    connector = aiohttp.TCPConnector(force_close=True)
    # connector = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            sensor_data = await response.read()
            sensor_json = json.loads(sensor_data)
            if len(sensor_json) > 0:
                return sensor_json[0]


def get_sensors_from_web():
    global sensors_from_web
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    all_sensors = [get("https://data.sensor.community/airrohr/v1/sensor/" + sens_id + '/') for sens_id in
                   sensor_per_country]
    results = loop.run_until_complete(asyncio.gather(*all_sensors))
    results = [i for i in results if i]
    sensors_from_web = results


# add here two parameters
def update_map(value_type, refresh=False):
    global sensors_from_web
    global sensor_df
    if sensors_from_web is None or refresh is True:
        get_sensors_from_web()
        sensor_df = pd.json_normalize(sensors_from_web, record_path='sensordatavalues', meta=['timestamp', 'location', 'sensor'])
        sensor_loc = pd.json_normalize(sensor_df['location'], meta=['latitude', 'longitude'])
        sensor_type = pd.json_normalize(sensor_df['sensor'], meta=['id', 'sensor_type'])
        sensor_df['latitude'] = sensor_loc['latitude'].astype(float)
        sensor_df['longitude'] = sensor_loc['longitude'].astype(float)
        sensor_df['sensor_id'] = sensor_type['id'].astype('i')

    typed_sensor_df = sensor_df.loc[sensor_df['value_type'] == value_type]

    typed_sensor_df["value"] = pd.to_numeric(typed_sensor_df["value"], downcast="float")

    fig = px.scatter_mapbox(typed_sensor_df, hover_name='value_type', lat="latitude", lon="longitude", color='value',
                            zoom=2,
                            height=850,
                            custom_data=['sensor_id'],
                            color_continuous_scale=[
                                [0.0, "blue"],
                                [0.1, "green"],
                                [0.3, "yellow"],
                                [1, "red"]]
                            )
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(clickmode='event+select')

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
    return fig


layout = html.Div([
    dbc.Row(
        [
            dbc.Col(html.Div([
        html.Label([
            "Type of Measurement:",
            dcc.Dropdown(
                id='type_of_measurement_id_worldmap',
                options=[
                    {'label': 'Temperature', 'value': 'temperature'},
                    {'label': 'Humidity', 'value': 'humidity'}
                ],
                value='',
                multi=False,
                className='form-select'
            ),
        ])
    ]), width=4, style={'text-align':'center'}),
            dbc.Col([html.Button('Refresh', id='submit_world', n_clicks=0, className='btn btn-primary'),
            ], width=2, style={'font': 'Lucida Console'}),
        ],
        justify="between",
        style={'margin-top':'1em'}
    ),
    dcc.Loading(children=[dcc.Graph(id='worldmap-graph-2', figure=emptyMap())], color='#ff5c33',
                type='cube'),
])
