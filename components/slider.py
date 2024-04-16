from dash import Dash, dcc, html, Input, Output, callback

import pandas as pd
import plotly.express as px
from utils.load_data import cleaned_games, genres, current_user_games
from utils.data_processing import get_n_best_gen_or_cat_by_hours, get_game_list_from_api

def steam_game_slider():
    games = current_user_games
    print(len(games))
    return dcc.Slider(
                0, #min value
                len(games), #max value
                step=5,
                id='user-playtime-slider',
                value=10,
            )

def genre_slider():
    return dcc.Slider(
                0, #min value
                len(genres['genres'].unique()), #max value
                step=1,
                id='genre-slider',
                value=5,
            )
