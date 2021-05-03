import dash
import dash_html_components as html
import dash_core_components as dcc

tabs_styles = {
    'height': '44px',
    'align-items': 'center'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-radius': '15px',
    'background-color': '#F2F2F2',
    'box-shadow': '4px 4px 4px 4px lightgrey',

}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px',
    'border-radius': '15px',
}

html.Div([
    html.Div([
        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='Tab 1', value='tab-1', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab 2', value='tab-2', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab 3', value='tab-3', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab 4', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
        html.Div(id='tabs-content-inline')
    ], className="create_container3 eight columns", ),
], className="row flex-display"),

html.Div([
    html.Div([
        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='Tab 1', value='tab-1', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab 2', value='tab-2', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab 3', value='tab-3', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Tab 4', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
        html.Div(id='tabs-content-inline')
    ], className="create_container3 eight columns", ),
], className="row flex-display"),

Python
app.d_lay = html.Div((

    html.Div([
        html.Div([
            html.Div([
                html.H3('Sales Data Analysis', style={'margin-bottom': '0px', 'color': 'black'}),
            ])
        ], className="create_container1 four columns", id="title"),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
                dcc.Tab(label='Tab 1', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Tab 2', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Tab 3', value='tab-3', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Tab 4', value='tab-4', style=tab_style, selected_style=tab_selected_style),
            ], style=tabs_styles),
            html.Div(id='tabs-content-inline')
        ], className="create_container3 eight columns", ),
    ], className="row flex-display"),

    html.Div([
        html.Div([

            html.P('Select Country', className='fix_label',
                   style={'color': 'black', 'margin-top': '2px', 'display': 'None'}),
            dcc.Dropdown(id='select_countries',
                         multi=False,
                         clearable=True,
                         disabled=False,
                         style={'display': 'None'},
                         value='Switzerland',
                         placeholder='Select Countries',
                         options=[{'label': c, 'value': c}
                                  for c in (income['Country'].unique())], className='dcc_compon'),

        ], className="create_container3 four columns", style={'margin-bottom': '20px'}),
    ], className="row flex-display"),

    html.Div([
        html.Div([
            html.P('Select Chart Type', className='fix_label', style={'color': 'black', 'display': 'None'}),
            dcc.RadioItems(id='radio_items',
                           labelStyle={"display": "inline-block"},
                           options=[
                               {'label': 'Line chart', 'value': 'line'},
                               {'label': 'Donut chart', 'value': 'donut'},
                               {'label': 'Horizontal bar chart', 'value': 'horizontal'}],
                           value='line',
                           style={'text-align': 'center', 'color': 'black', 'display': 'None'}, className='dcc_compon'),

            dcc.Graph(id='multi_chart',
                      style={'display': 'None'},
                      config={'displayModeBar': 'hover'}),

        ], className="create_container3 six columns"),

    ], className="row flex-display"),

    html.Div([
        html.Div([

            html.P('Select Chart Type', className='fix_label', style={'color': 'black', 'display': 'None'}),
            dcc.RadioItems(id='radio_items1',
                           labelStyle={"display": "inline-block"},
                           options=[
                               {'label': 'Line chart', 'value': 'line'},
                               {'label': 'Donut chart', 'value': 'donut'},
                               {'label': 'Horizontal bar chart', 'value': 'horizontal'}],
                           value='line',
                           style={'text-align': 'center', 'color': 'black', 'display': 'None'}, className='dcc_compon'),

            # html.P('Select Country', className = 'fix_label', style = {'color': 'black', 'margin-top': '2px', 'display': 'None'}),
            # dcc.Dropdown(id = 'select_countries1',
            #              multi = False,
            #              clearable = True,
            #              disabled = False,
            #              style = {'display': 'None'},
            #              value = 'Switzerland',
            #              placeholder = 'Select Countries',
            #              options = [{'label': c, 'value': c}
            #                         for c in (income['Country'].unique())], className = 'dcc_compon'),

        ], className="create_container3 four columns", style={'margin-bottom': '20px'}),
    ], className="row flex-display"),

    html.Div([
        html.Div([

            dcc.Graph(id='multi_chart1',
                      style={'display': 'None'},
                      config={'displayModeBar': 'hover'}),
        ], className="create_container3 six columns"),
    ], className="row flex-display"),

), id="mainContainer", style={"display": "flex", "flex-direction": "column"})

app.d_lay = html.Div((

    html.Div([
        html.Div([
            html.Div([
                html.H3('Sales Data Analysis', style={'margin-bottom': '0px', 'color': 'black'}),
            ])
        ], className="create_container1 four columns", id="title"),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
                dcc.Tab(label='Tab 1', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Tab 2', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Tab 3', value='tab-3', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Tab 4', value='tab-4', style=tab_style, selected_style=tab_selected_style),
            ], style=tabs_styles),
            html.Div(id='tabs-content-inline')
        ], className="create_container3 eight columns", ),
    ], className="row flex-display"),

    html.Div([
        html.Div([

            html.P('Select Country', className='fix_label',
                   style={'color': 'black', 'margin-top': '2px', 'display': 'None'}),
            dcc.Dropdown(id='select_countries',
                         multi=False,
                         clearable=True,
                         disabled=False,
                         style={'display': 'None'},
                         value='Switzerland',
                         placeholder='Select Countries',
                         options=[{'label': c, 'value': c}
                                  for c in (income['Country'].unique())], className='dcc_compon'),

        ], className="create_container3 four columns", style={'margin-bottom': '20px'}),
    ], className="row flex-display"),

    html.Div([
        html.Div([
            html.P('Select Chart Type', className='fix_label', style={'color': 'black', 'display': 'None'}),
            dcc.RadioItems(id='radio_items',
                           labelStyle={"display": "inline-block"},
                           options=[
                               {'label': 'Line chart', 'value': 'line'},
                               {'label': 'Donut chart', 'value': 'donut'},
                               {'label': 'Horizontal bar chart', 'value': 'horizontal'}],
                           value='line',
                           style={'text-align': 'center', 'color': 'black', 'display': 'None'}, className='dcc_compon'),

            dcc.Graph(id='multi_chart',
                      style={'display': 'None'},
                      config={'displayModeBar': 'hover'}),

        ], className="create_container3 six columns"),

    ], className="row flex-display"),

    html.Div([
        html.Div([

            html.P('Select Chart Type', className='fix_label', style={'color': 'black', 'display': 'None'}),
            dcc.RadioItems(id='radio_items1',
                           labelStyle={"display": "inline-block"},
                           options=[
                               {'label': 'Line chart', 'value': 'line'},
                               {'label': 'Donut chart', 'value': 'donut'},
                               {'label': 'Horizontal bar chart', 'value': 'horizontal'}],
                           value='line',
                           style={'text-align': 'center', 'color': 'black', 'display': 'None'}, className='dcc_compon'),

            # html.P('Select Country', className = 'fix_label', style = {'color': 'black', 'margin-top': '2px', 'display': 'None'}),
            # dcc.Dropdown(id = 'select_countries1',
            #              multi = False,
            #              clearable = True,
            #              disabled = False,
            #              style = {'display': 'None'},
            #              value = 'Switzerland',
            #              placeholder = 'Select Countries',
            #              options = [{'label': c, 'value': c}
            #                         for c in (income['Country'].unique())], className = 'dcc_compon'),

        ], className="create_container3 four columns", style={'margin-bottom': '20px'}),
    ], className="row flex-display"),

    html.Div([
        html.Div([

            dcc.Graph(id='multi_chart1',
                      style={'display': 'None'},
                      config={'displayModeBar': 'hover'}),
        ], className="create_container3 six columns"),
    ], className="row flex-display"),

), id="mainContainer", style={"display": "flex", "flex-direction": "column"})

