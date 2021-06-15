import dash_core_components as dcc
import dash_html_components as html
from datetime import date as dt, timedelta
import dash
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime
import json

# import warnings
# warnings.filterwarnings('ignore')


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