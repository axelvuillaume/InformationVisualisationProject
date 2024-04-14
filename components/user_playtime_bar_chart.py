from dash import Dash, dcc, html, Input, Output, callback

import pandas as pd
import plotly.express as px
from utils.load_data import cleaned_games, genres
from utils.data_processing import get_n_best_gen_or_cat_by_hours, get_game_list_from_api

def playtime_per_genre(steamid, genres_amount=4, games_amount=10):
    games = get_game_list_from_api(steamid)

    # Get the top 8 genres by playtime
    top_n_genres = list(get_n_best_gen_or_cat_by_hours(games, genres, n=genres_amount).keys())
    filtered_genres = genres[genres['genres'].isin(top_n_genres)]

    games = games.join(filtered_genres.set_index('app_id'), on='app_id', how='inner')
    games = games.join(cleaned_games[['name', 'app_id']].set_index('app_id'), on='app_id', how='inner')
    games = games.drop_duplicates(subset='app_id', keep='first') # Only assign one genre to each game (some games have multiple genres)
    games['playtime_forever'] = games['playtime_forever'] / 60
    if(games_amount > 0):
        games = games.head(games_amount)

    fig = px.bar(games, x="genres", y="playtime_forever", color="name", text="name", title="User Playtime Chart")
    fig.update_layout(yaxis_title="Playtime (hours)", xaxis_title="Genre")
    return dcc.Graph(id='playtime-bar-chart-figure',figure=fig)