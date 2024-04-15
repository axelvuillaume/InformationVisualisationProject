from dash import Dash, dcc, html, Input, Output, callback

import pandas as pd
import plotly.express as px
from components.top_games_chart import generate_top_games_chart

from components.hexagon import hexagon
from components.bubble_chart import bubble_chart
from components.user_playtime_bar_chart import playtime_per_genre
from components.slider import steam_game_slider, genre_slider
from utils.load_data import cleaned_games, categories, genres, supported_languages, full_audio_languages
from utils.data_processing import get_n_best_gen_or_cat_by_hours, get_game_list_from_api

def generate_home_layout():
    return html.Div(
        id='main-canva',
        children=[
            html.H1('STEAM DASHBOARD'),

            html.Div([
                "Steam Id: ",
                dcc.Input(id='steam-id', placeholder="Insert Steam Id", value='76561198150561997'),
            ], style={'color': 'white'}),

            html.Div(
                className="component-container",
                children=[
                    generate_top_games_chart(cleaned_games, n=10)
                ]
            ),
            html.Div(
                className="component-container",
                id = 'hexagon',
                children=[
                    #hexagon(categories, genres, n=8)
                ]
            ),
            html.Div(
                className="component-container",
                id = 'bubble-chart',
                children=[
                    #bubble(n=8)
                ]
            ),
            
                id = 'user-playtime-chart',
                children=[
                    html.Div(
                        id = 'user-playtime-chart',
                    ),
                    html.Div(
                        style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'flex-start', 'align-items': 'center'},
                        children=[
                            html.H4("Game Amount: ", style={'color': 'white'}),
                            html.Div(
                                id = 'user-game-slider',
                                style={'width': '80%', 'margin-top': '1em'}
                            )
                        ]
                    ),
                    html.Div(
                        style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'flex-start', 'align-items': 'center'},
                        children=[
                            html.H4("Genre Amount: ", style={'color': 'white'}),
                            html.Div(
                                id = 'genre-slider',
                                style={'width': '80%', 'margin-top': '1em'},
                                children=[
                                    genre_slider()
                                ]
                            )
                        ]
                    )
                    ,
                  html.Div(
                    className="component-container",
                    children=[
                        html.Div(
                            className="component-container",
                                children=[foo("price", "categories")[0]]
                            ),
                        html.Div(
                            className="component-container",
                            children=[foo("price", "categories")[1]]
                            ),
                        html.Div(
                            className="component-container",
                            children=[foo("price", "categories")[2]]
                            ),
                    ]
                )
               ],
            ),
        ]
    )

@callback(
    Output('hexagon', "children"),
    Input("steam-id", "value"),
)
def compute_hexagon(steam_id):
    return hexagon(categories, genres, steam_id, n=8)

@callback(
    Output('bubble-chart', "children"),
    Input("steam-id", "value"),
)
def bubble(steam_id):
    return bubble_chart(steam_id)

@callback(
    Output('user-playtime-chart', "children"),
    Input("steam-id", "value"),
    Input("user-playtime-slider", "value"),
    Input("genre-slider", "value"),
)
def playtime_chart(steam_id, games_slider_value, genre_slider_value):
    return playtime_per_genre(steam_id, games_amount=games_slider_value, genres_amount=genre_slider_value)

@callback(
    Output('user-game-slider', "children"),
    Input("steam-id", "value"),
)
def playtime_slider(steam_id):
    return steam_game_slider(steam_id)
