from dash import dcc, html, Input, Output, callback

import plotly.express as px
from utils.load_data import cleaned_games

options = [  # Define options outside the dcc.Dropdown call
    {'label': "Price", 'value': "price"},
    {'label': "Metacritic score", 'value': "metacritic_score"},
    {'label': 'User score', 'value': 'user_score'},
    {'label': 'Average playtime forever', 'value': 'average_playtime_forever'},
    {'label': 'Score', 'value': 'score'},
]

def graph_comparaison():
    return html.Div([
        html.Div([html.Div(children='X axis :', style={'color': 'white', 'padding-bottom': '1em'}),
                         dcc.Dropdown(id='x-axis-selector', options=options, value='price')
                        ],
                 style={'width': '50%', 'display': 'inline-block'}
                ),

        # Y-axis selector
        html.Div([html.Div(children='Y axis :' ,   style={ 'color': 'white', 'padding-bottom': '1em'}),
                         dcc.Dropdown(id='y-axis-selector',
                                      options=options,
                                      value='average_playtime_forever'
                                     ),
                        ],
                 style={'width': '50%', 'display': 'inline-block'}
                ),

        dcc.Graph(id='graph')
    ])

@callback(Output('graph', 'figure'),
          [Input('x-axis-selector', 'value'),
           Input('y-axis-selector', 'value')
          ])

def update_graph(x_column, y_column):
    grouped_df = cleaned_games.groupby(x_column)[y_column].mean().reset_index()
    merged_df = grouped_df.merge(cleaned_games[[x_column, 'name']], on=x_column, how='left')
    fig = px.line(merged_df, x=x_column, y=y_column, hover_name="name", title=f"Comparaison of {y_column} according to {x_column}", )
    return fig