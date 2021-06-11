# import numpy as np
# import pandas as pd
# import dash
import dash_core_components as dcc
import dash_html_components as html
# import warnings
# warnings.filterwarnings('ignore')

from layouts import layout_clustering


layout = html.Div([
    layout_clustering,
    dcc.Graph(id='output-container-clustering', style={'height': '90vh'})
], )