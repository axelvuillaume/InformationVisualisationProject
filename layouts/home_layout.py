from dash import Dash, dcc, html, Input, Output, callback, State
import json
import pandas as pd
import plotly.express as px

import dash_bootstrap_components as dbc

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

def generate_home_layout():
    return html.Div(
        className ="wrapper",
        id='main-canva',
        children=[
            
            html.Div([
            html.H1('STEAM DASHBOARD'),
                dcc.Link('Home', href='/home', id='home-link', className='button'),
                dcc.Link('Profile', href='/profile', id='profile-link', className='button')
        ], className='button-container one'),

            
            # once update-user-data is finished, store the steam id, once this changes the graph updates are triggered
            # see example 1 for more info : https://dash.plotly.com/sharing-data-between-callbacks



        
            html.Div(
                className="component-container two",
                children=[
                    generate_top_games_chart(cleaned_games, n=10)
                ]
            ),

            html.Div(
                className="component-container three",
                id = 'gauges',
                children=[
                    html.Div(
                    className="component-container",
                    children=[
                        html.Div(
                            className="component-container",
                                children=[gauge_percentages("positive", "full_audio_languages")[0]]
                            ),
                        html.Div(
                            className="component-container",
                            children=[gauge_percentages("positive", "full_audio_languages")[1]]
                            ),
                        html.Div(
                            className="component-container",
                            children=[gauge_percentages("positive", "full_audio_languages")[2]]
                            ),
                    ]
                )
                ]
            ),
            html.Div(
                className="component-container four",
                id='sunburst_by_categries',
                children=[
                    graph_sunburst()
            ]
            ),
            html.Div(
                className="component-container five",
                id='map_by_supported_languages',
                children=[
                    graph_map()
            ]
            ),
        ]
    )
    
@callback(
    Output('home-link', 'className'),
    Output('profile-link', 'className'),
    Input('url', 'pathname')
)
def update_links(pathname):
    home_class = 'button active' if pathname == '/home' else 'button'
    profile_class = 'button active' if pathname == '/profile' else 'button'
    return home_class, profile_class
