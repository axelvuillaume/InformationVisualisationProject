from dash import Dash, dcc, html, Input, Output, callback,dash_table

import pandas as pd
import plotly.express as px
from utils.load_data import cleaned_games, genres, current_user,categories
from utils.data_processing import get_n_best_gen_or_cat_by_hours, get_game_list_from_api


options = [  # Define options outside the dcc.Dropdown call
    {'label': "Price", 'value': "price"},
    {'label': "Metacritic score", 'value': "metacritic_score"},
    {'label': 'User score', 'value': 'user_score'},
    {'label': 'Average playtime forever', 'value': 'average_playtime_forever'},
    {'label': 'Score', 'value': 'score'},
]

def graph_comparaison():
    return html.Div([
        
      
        
        html.Div([
            html.Div(children='X axis :',   style={ 
            'color': 'white', 'padding-bottom': '1em'
        }),
            dcc.Dropdown(
                id='x-axis-selector',
                options=options,
                value='price'
            ),
        ], style={'width': '50%', 'display': 'inline-block'}),


            
        # Y-axis selector
        html.Div([
            html.Div(children='Y axis :' ,   style={ 
            'color': 'white', 'padding-bottom': '1em'
        }),
            dcc.Dropdown(
                id='y-axis-selector',
                options=options,
                value='average_playtime_forever'
            ),
        ], style={'width': '50%', 'display': 'inline-block'}),
        
          dcc.Graph(id='graph'),
    ])



# Callback pour mettre à jour le graphique en fonction des sélections des boutons radio
@callback(
    Output('graph', 'figure'),
    [Input('x-axis-selector', 'value'),
     Input('y-axis-selector', 'value')]
)

def update_graph(x_column, y_column):
    grouped_df = cleaned_games.groupby(x_column)[y_column].mean().reset_index()
    fig = px.line(grouped_df, x=x_column, y=y_column, title=f"Comparaison de {y_column} selon {x_column}" )
    return fig