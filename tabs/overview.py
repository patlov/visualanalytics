# import numpy as np
# import pandas as pd
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import warnings
# warnings.filterwarnings('ignore')
#
# global_temp_country = pd.read_csv('archive/GlobalLandTemperaturesByCountry.csv')
#
# global_temp_country_clear = global_temp_country[~global_temp_country['Country'].isin(
#     ['Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands',
#      'United Kingdom', 'Africa', 'South America'])]
#
# global_temp_country_clear = global_temp_country_clear.replace(
#     ['Denmark (Europe)', 'France (Europe)', 'Netherlands (Europe)', 'United Kingdom (Europe)'],
#     ['Denmark', 'France', 'Netherlands', 'United Kingdom'])
#
# # Let's average temperature for each country
#
# countries = np.unique(global_temp_country_clear['Country'])
# mean_temp = []
# for country in countries:
#     mean_temp.append(global_temp_country_clear[global_temp_country_clear['Country'] ==
#                                                country]['AverageTemperature'].mean())
#
# data = [dict(
#     type='choropleth',
#     locations=countries,
#     z=mean_temp,
#     locationmode='country names',
#     text=countries,
#     marker=dict(
#         line=dict(color='rgb(0,0,0)', width=1)),
#     colorbar=dict(autotick=True, tickprefix='',
#                   title='# Average\nTemperature,\n°C')
# )
# ]
#
# d_lay = dict(
#     title='Average land temperature in countries',
#     geo=dict(
#         showframe=False,
#         showocean=True,
#         oceancolor='rgb(0,255,255)',
#         projection=dict(
#             type='orthographic',
#             rotation=dict(
#                 lon=60,
#                 lat=10),
#         ),
#         lonaxis=dict(
#             showgrid=True,
#             gridcolor='rgb(102, 102, 102)'
#         ),
#         lataxis=dict(
#             showgrid=True,
#             gridcolor='rgb(102, 102, 102)'
#         )
#     ),
# )
#
# fig = dict(data=data, layout=d_lay)
#
# layout = html.Div([
#     dcc.Graph(
#         id='example-graph-2',
#         figure=fig
#     ),
#     html.Div(id='page-2-content')
# ])