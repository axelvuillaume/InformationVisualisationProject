from dash import Dash, dcc, html, Input, Output, callback, State
import json
import pandas as pd
import plotly.express as px
from components.top_games_chart import generate_top_games_chart

from components.user_vs_friends_panel import generate_user_vs_friends_panel
from components.bubble_chart import bubble_chart
from components.user_playtime_bar_chart import playtime_per_genre, playtime_games_per_genre
from components.slider import steam_game_slider, genre_slider
from components.gauge import gauge_percentages
from components.map import graph_map
from components.sunburst import graph_sunburst
from utils.load_data import cleaned_games, categories, genres, current_user, supported_languages, full_audio_languages
from utils.data_processing import get_n_best_gen_or_cat_by_hours, get_game_list_from_api

def generate_profile_layout():
    return html.Div(
        id='main-canva',
        children=[
            html.Div([
            html.H1('PROFILE STEAM DASHBOARD'),
                dcc.Link('Home', href='/home', id='home-link', className='button'),
                dcc.Link('Profile', href='/profile', id='profile-link', className='button')
        ], className='button-container',style={'width': '100%'} ),
        ]
    )
    
