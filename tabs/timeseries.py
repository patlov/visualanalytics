from datetime import date
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

layout = html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=date(2017, 9, 19),
        initial_visible_month=date(2017, 8, 5),
        end_date=date(2017, 8, 25)
    ),
    html.Div(id='output-container-date-picker-range')
])