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
    #get from cleaned_games the top 5 games of each genre in ranking, by score
    
    games_per_genre = []
    for gen in ranking:
        top_games_in_genre = cleaned_games[
             cleaned_games['app_id'].isin(
                 genres[genres['genres'] == gen]['app_id']
             )]
        top_games_in_genre = top_games_in_genre.nlargest(5, 'score')[['name', 'price', 'positive', 'negative', 'score', 'median_playtime_forever']]
        top_games_in_genre['genre'] = gen
        games_per_genre += top_games_in_genre.values.tolist()
    
    # for gen in ranking:
    #     random_games_in_genre = cleaned_games[
    #         cleaned_games['app_id'].isin(
    #             genres[genres['genres'] == gen]['app_id'].head(5)
    #         )
    #     ][['name', 'price', 'positive', 'negative']]
    #     random_games_in_genre['genre'] = gen
    #     games_per_genre += random_games_in_genre.values.tolist()

    df = pd.DataFrame(games_per_genre)
    df.columns=['name', 'price', 'positive reviews', 'negative reviews', 'score', 'median playtime', 'genre']

    # Add a column containing total number of reviews, 
    # NOTE: total reviews seems to be a better indicator of games sold than min_owners/max_owners 
    df['total reviews'] = df['positive reviews'] + df['negative reviews']

    # transform data to use the percentage of positive reviews
    df['positive reviews (%)'] = df['positive reviews']/(df['positive reviews'] + df['negative reviews']) * 100
   
    fig = px.scatter(df, x="median playtime", y="positive reviews (%)", size="score", 
                     color="genre", hover_name="name",
                     size_max=50)
    fig.update_layout(yaxis_title='Positive reviews (%)', xaxis_title='Median Playtime', title='Interesting games based on your favorite genres')
    return dcc.Graph(id='bubble-chart-figure',figure=fig)
