from dash import Dash, dcc, html, Input, Output, callback, State
import json
import pandas as pd
import plotly.express as px
from components.top_games_chart import generate_top_games_chart

from components.hexagon import hexagon
from components.bubble_chart import bubble_chart
from components.user_playtime_bar_chart import playtime_per_genre, playtime_games_per_genre
from components.slider import steam_game_slider, genre_slider
from components.gauge import gauge_percentages
from utils.load_data import cleaned_games, categories, genres, current_user, supported_languages, full_audio_languages
from utils.data_processing import get_n_best_gen_or_cat_by_hours, get_game_list_from_api

def generate_home_layout():
    return html.Div(
        id='main-canva',
        children=[
            html.H1('STEAM DASHBOARD'),

            dcc.Store(id='steam-id-store'), 
            # once update-user-data is finished, store the steam id, once this changes the graph updates are triggered
            # see example 1 for more info : https://dash.plotly.com/sharing-data-between-callbacks

            html.Div([
                "Steam Id: ",
                dcc.Input(id='steam-id', placeholder="Insert Steam Id", value='76561198150561997'),
                html.Button(id='submit-steamid', n_clicks=0, children='Submit')
            ], style={'color': 'white'}),

            html.Div(
                className="component-container",
                children=[
                    generate_top_games_chart(cleaned_games, n=10)
                ]
            ),
            html.Div(
                className="component-container",
                id='hexagonContainer',
                children=[
                    html.Div(
                        children=[
                        html.H2("User Vs Friends Profile", style={'color': 'white'}),
                        html.Div(
                            id='hexagon-menu',
                            children=[
                                html.H4("Number of sides:", style={'color': 'white','padding-left': '0.5em','padding-right': '0.5em'}),
                                dcc.Dropdown(
                                    id='side-selector',
                                    options=[
                                        {'label': str(i), 'value': i} for i in range(5, 9)
                                    ],
                                    value=6,  #default value
                                    clearable=False,
                                    searchable=False,
                                    style={'width': 'auto','align-self': 'center','padding-left': '0.5em','padding-right': '0.5em'}
                                ),
                                html.H4("Types:", style={'color': 'white','padding-left': '0.5em','padding-right': '0.5em'}),
                                dcc.RadioItems(
                                    id='chart-type',
                                    options=[
                                        {'label': 'Categories', 'value': 'categories'},
                                        {'label': 'Genres', 'value': 'genres'}
                                    ],
                                    value='categories',  #default value
                                    labelStyle={'color': 'white'},
                                    style={'width': 'auto','align-self': 'center','padding-left': '0.5em','padding-right': '0.5em'}
                                )
                            ],
                            style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between' , 'width': '400px','background-color': '#171D25'}
                        ),
                        html.Div(id='hexagon')
                        ],
                        style={'display': 'flex', 'flex-direction': 'column','width': '25%'}
                    )
                ]
            ),
            html.Div(
                className="component-container",
                id = 'bubble-chart',
                children=[
                    #bubble(n=8)
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
            html.Div(
                className="component-container",
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
    Output('hexagon', "children"),
    [Input('steam-id-store', 'data'),
     Input('side-selector', 'value'),
     Input('chart-type', 'value')]
)
def compute_hexagon(_, n, category_select):
    return hexagon(categories, genres, category_select=category_select, n=n)

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
