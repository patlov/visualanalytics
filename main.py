import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from tabs import timeseries
from tabs import worldmap
from tabs import overview

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
@app.callback(dash.dependencies.Output('page-1-content', 'children'), [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)


# Worldmap
@app.callback(Output('page-2-content', 'children'), [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
