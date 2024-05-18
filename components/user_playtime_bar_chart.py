from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from utils.load_data import cleaned_games, genres, current_user
from utils.data_processing import get_n_best_gen_or_cat_by_hours, get_game_list_from_api
from components.alert import alert
def playtime_per_genre(genres_amount=4, games_amount=10):
    games = current_user.games
    
    # Get the top 8 genres by playtime
    top_n_genres = list(get_n_best_gen_or_cat_by_hours(games, genres, n=genres_amount).keys())
    filtered_genres = genres[genres['genres'].isin(top_n_genres)]

    games = games.join(filtered_genres.set_index('app_id'), on='app_id', how='inner')
    games = games.join(cleaned_games[['name', 'app_id']].set_index('app_id'), on='app_id', how='inner')
    
    # Shuffle the entries, so the same genre doesn't always show up first
    # Then drop duplicates based on app_id so each game only belongs to 1 genre
    games = games.sample(frac=1).drop_duplicates(subset='app_id')

    # Alternatively assign only first genre encountered (which means most games will end up in the same genre)
    # games = games.drop_duplicates(subset='app_id', keep='first')
    
    games['playtime_forever'] = games['playtime_forever'] / 60

    games = games.sort_values('playtime_forever', ascending=True) 
    # As you increase the slider, bigger blocks of games start showing up, which makes the
    # lesser played games harder to see. This is why we sort the games by playtime, so the
    # lesser played games are still visible if you decrease game_amount
    
    if(games_amount > 0):
        games = games.head(games_amount)

    fig = px.bar(games, x="genres", y="playtime_forever", custom_data=["app_id"], color="genres", text="name", title="User Playtime Chart")
    fig.update_layout(yaxis_title="Playtime (hours)", xaxis_title="Genre")

    g =  dcc.Graph(id='playtime-bar-chart-figure',figure=fig)
    a = alert(6)

    return html.Div([a, g])

def playtime_games_per_genre(genre_name):
    # TODO: extract duplicate code with previous function into a separate function
    if genre_name is not None:
        games = current_user.games
        filtered_genres = genres[genres['genres'] == genre_name]

        games = games.join(filtered_genres.set_index('app_id'), on='app_id', how='inner')
        games = games.join(cleaned_games[['name', 'app_id']].set_index('app_id'), on='app_id', how='inner')
        games['playtime_forever'] = round(games['playtime_forever'] / 60, 2)
        games['playtime_formatted'] = games['playtime_forever'].map(lambda playtime: f"{int(playtime):02d}:{int((playtime*60) % 60):02d}")
        games.sort_values('playtime_forever', ascending=True, inplace=True)

        fig = go.Figure(
            data=go.Bar(
                    x=games["playtime_forever"],
                    text=games["playtime_formatted"],  
                ),
            layout={
                'bargroupgap':0.4,
                # 'height': 2000, enable with scrollbar for bigger bars
                'yaxis':{'visible': False},
            }
        )
        for idx, name in enumerate(games["name"]): 
            fig.add_annotation(
                x=0,
                y=idx + 0.45,
                text=name,
                xanchor='left',
                showarrow=False,
                yshift=0
        )
        # fig = px.bar(games, x="playtime_forever", y="name", text="playtime_formatted", orientation='h',
        #              title=f"Playtimes for genre: {genre_name}")
        
        fig.update_layout(yaxis_title="Game", xaxis_title="Playtime (hours)", title=f"Playtimes for genre: {genre_name}")
        # fig.update_traces(textangle=0, textposition="outside", cliponaxis=False, hovertemplate="Game: %{y}<br>Playtime: %{x} hours")
        return dcc.Graph(id='detail-playtime-figure', figure=fig, style={'height': '100%'})
    else:
        return dcc.Markdown(
            "### Select a genre on the 'User Playtime Chart' to see the playtimes for that genre",
            style={'color': 'white', 'padding': '1em'}
            )
