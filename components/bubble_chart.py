from dash import Dash, dcc, html, Input, Output, callback

import pandas as pd
import plotly.express as px
from utils.load_data import cleaned_games, genres, current_user
from utils.data_processing import get_n_best_gen_or_cat_by_hours, get_game_list_from_api
from components.alert import alert
"""
A bubble plot to recommend games based on 4 different features, chosen
from: 'price', 'positive reviews', 'negative reviews', 'score', 'median playtime', 'genre', 
'positive reviews (%)', 'total reviews

:param x_label: label for x axis
:param y_label: label for y axis
:param title: title for the plot
:param x_axis: column describing x-axis values
:param y_axis: column describing y-axis values
:param size_col: column deciding size of markers
:param color_col: column deciding colors of the markers
:return: Bubble plot figure
"""
def bubble_chart(y_label='Positive reviews (%)', x_label='Price', title='Interesting games based on your favorite genres',
                 x_axis="price", y_axis="positive reviews (%)", size_col="total reviews", color_col="genre"):
    games = current_user.games
    ranking = get_n_best_gen_or_cat_by_hours(games, genres, n=8)

    #get from cleaned_games the top 5 games of each genre in ranking, by score
    games_per_genre = []
    for gen in ranking:
        top_games_in_genre = cleaned_games[
             cleaned_games['app_id'].isin(
                 genres[genres['genres'] == gen]['app_id']
             ) & ~cleaned_games['app_id'].isin(current_user.games['app_id'])
        ]
        top_games_in_genre = top_games_in_genre.nlargest(5, 'score')[['name', 'price', 'positive', 'negative', 'score', 'median_playtime_forever']]
        top_games_in_genre['genre'] = gen
        games_per_genre += top_games_in_genre.values.tolist()

    df = pd.DataFrame(games_per_genre)
    df.columns=['name', 'price', 'positive reviews', 'negative reviews', 'score', 'median playtime', 'genre']

    # Add a column containing total number of reviews, 
    # NOTE: total reviews seems to be a better indicator of games sold than min_owners/max_owners 
    df['total reviews'] = df['positive reviews'] + df['negative reviews']

    # transform data to use the percentage of positive reviews
    df['positive reviews (%)'] = df['positive reviews']/(df['positive reviews'] + df['negative reviews']) * 100
   
    fig = px.scatter(df, x=x_axis, y=y_axis, size=size_col, 
                     color=color_col, hover_name="name", #log_x=True,
                     size_max=50)
    fig.update_layout(yaxis_title=y_label, xaxis_title=x_label, title=title)
    #fig.update_traces(marker_size=15)

    g = dcc.Graph(id='bubble-chart-figure',figure=fig)
    a = alert(5)
    return html.Div([a, g])
