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
from components.alert import alert

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
            
        
        dcc.Store(id='steam-id-store'), 
        
        
            html.Div([
                "Steam Id: ",
                dcc.Input(id='steam-id', placeholder="Insert Steam Id", value='76561198150561997'),
                html.Button(id='submit-steamid', n_clicks=0, children='Submit')
            ], style={'color': 'white'}),
            
                        html.Div(
                className="component-container",
                id='user_vs_friends_panel',
                children=[alert(4),
                          generate_user_vs_friends_panel()
                         ]
            ),

            html.Div(
                className="component-container",
                id = 'bubble-chart',
                children=[#bubble(n=8)
                         ]
            ),

            html.Div(
                className="component-container",
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
                    # TODO: check if we need the genre slider else remove
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
                    ),
               ],
            ),
            html.Div(
                className="component-container",
                id = 'detail-playtime-chart',
                children=[
                ]
            ),
        ]
    )
    

@callback(
    Output('steam-id-store', 'data'),
    Input("submit-steamid", "n_clicks"),
    State("steam-id", "value"),
    running=[(Output("submit-steamid", "disabled"), True, False)] 
    #While callback is running -> button property disabled = True; when done, disabled = False
)
def update_current_user(_, steamid):
    current_user.steamid = steamid
    return steamid

@callback(
    Output('bubble-chart', "children"),
    Input('steam-id-store', 'data')
)
def bubble(_):
    return bubble_chart()

@callback(
    Output('user-playtime-chart', "children"),
    Input('steam-id-store', 'data'),
    Input("user-playtime-slider", "value"),
    Input("genre-slider", "value")
)
def playtime_chart(_, games_slider_value, genre_slider_value):
    return playtime_per_genre(games_amount=games_slider_value, genres_amount=genre_slider_value)

@callback(
    Output('user-game-slider', "children"),
    Input('steam-id-store', 'data')
)
def playtime_slider(_):
    return steam_game_slider()

@callback(
    Output('detail-playtime-chart', 'children'),
    Input('playtime-bar-chart-figure', 'clickData'))
def display_click_data(clickData):
    # 'x' key of the clickData contains the genre name
    genre_name = clickData['points'][0]['x'] if clickData else None
    return playtime_games_per_genre(genre_name)