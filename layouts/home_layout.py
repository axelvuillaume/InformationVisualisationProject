from dash import Dash, dcc, html, Input, Output, callback

import pandas as pd
import plotly.express as px
from components.top_games_chart import generate_top_games_chart
from components.hexagon import hexagon
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
    games = get_game_list_from_api(steam_id)
    ranking = get_n_best_gen_or_cat_by_hours(games, genres, n=8)
    games_per_genre = []
    for gen in ranking:
        # games_per_genre[gen] = 
        random_games_in_genre = cleaned_games[
                cleaned_games['app_id'].isin(
                genres[genres['genres'] == gen]['app_id'].head(5)
                )][['name', 'price', 'max_owners', 'positive']]
        random_games_in_genre['genre'] = gen
        games_per_genre += random_games_in_genre.values.tolist()
        # print(random_games_in_genre.values.tolist())
        # games_per_genre.append(random_games_in_genre.values.tolist())
        # print(games_per_genre)
    df = pd.DataFrame(games_per_genre)
    df.columns=['name', 'price', 'max_owners', 'positive', 'genre']

    fig = px.scatter(df, x="price", y="positive",
                 size="max_owners", color="genre", hover_name="name", 
                 #log_x=True, 
                 size_max=60)
    # print(df)
    # return html.Div("hello")
    return dcc.Graph(id='bubble-chart-figure',figure=fig)

