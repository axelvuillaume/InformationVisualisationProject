from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from utils.load_data import cleaned_games, genres, current_user
from utils.data_processing import get_n_best_gen_or_cat_by_hours, get_game_list_from_api, get_achievements_for_game
from components.alert import alert
from datetime import datetime

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

def achievement_chart(app_id, game_name):

    if(app_id is not None):
        achievement_data = get_achievements_for_game(current_user.steamid , app_id)
        global_achievements = achievement_data['global_achievements']
        achievement_list = [{"global_percent": [g_achievement['percent'] for g_achievement in global_achievements if g_achievement['name'] == achievement['apiname']][0], 
                            "name": achievement['name'], "unlocktime": achievement['unlocktime'], 
                            "unlocktime_datetime": datetime.fromtimestamp(achievement['unlocktime']).strftime('%d/%m/%y %H:%M') } 
                            for achievement in achievement_data['achievements'] 
                            if achievement['achieved'] == 1]
        if achievement_list:
            achievement_df = pd.DataFrame(achievement_list)
            achievement_df.sort_values('unlocktime', ascending=True, inplace=True)
            achievement_df['achievement_index'] = range(1, len(achievement_df) + 1)
            # achievement_df['percentage_rank_symbols'] = achievement_df['global_percent'].map(
            #     lambda x: 1 if(x <= 1)
            #     else 2 if (x <= 5) 
            #     else 3 if (x <= 10) 
            #     else 4 if (x <= 50) 
            #     else 5)
            # achievement_df['percentage_rank_colors'] = achievement_df['global_percent'].map(
            #     lambda x: "#003f5c" if(x <= 1)
            #     else "#58508d" if (x <= 5) 
            #     else "#bc5090" if (x <= 10) 
            #     else "#ff6361" if (x <= 50) 
            #     else "#ffa600")
            # # used this to decide the colors https://www.learnui.design/tools/data-color-picker.html#palette
            achievement_df['percentage_rank_name'] = achievement_df['global_percent'].map(
                lambda x: "very rare (0%, 1%]" if(x <= 1)
                else "rare (1%, 5%]" if (x <= 5) 
                else "uncommon (5%, 10%]" if (x <= 10) 
                else "common (10%, 50%]" if (x <= 50) 
                else "very common (50%, 100%]")

            # Alternate version with lines
            # fig = px.line(achievement_df, x='unlocktime_datetime', y='global_percent', 
            #             #   color="percentage_rank_name",  
            #               markers=True, 
            #               #text=achievement_df['name']
            #               )
            # fig.update_traces(marker=dict(size=12, 
            #                                color=achievement_df['percentage_rank_colors'], 
            #                                symbol=achievement_df['percentage_rank_symbols'],
            #                             #   cmin=1, 
            #                             #   cmax=5
            #                               ),
            #                     textposition="bottom right")

            fig = px.scatter(achievement_df, x='unlocktime_datetime', y='global_percent', 
                            color="percentage_rank_name",
                            symbol="percentage_rank_name",
                            category_orders={"percentage_rank_name": 
                                            ["very rare (0%, 1%)",
                                            "rare (1%, 5%)",
                                            "uncommon (5%, 10%)",
                                            "common (10%, 50%)",
                                            "very common (50%, 100%)"]},
                            color_discrete_sequence=px.colors.qualitative.Bold,
                            hover_data=["name"],
                            labels={"percentage_rank_name": "Rarity", "unlocktime_datetime": "Unlock time", 'global_percent': "Global Percentage", "name": "Achievement Name"}
                            # text=achievement_df['name']
                            )
            fig.update_traces(marker=dict(size=12,
                                        #   color=achievement_df['percentage_rank_colors'], 
                                        ),
                                # textposition="bottom right",
                                showlegend=True)
            
            fig.update_layout(yaxis=dict(autorange="reversed"), yaxis_title="Global Percentage", xaxis_title="Unlock Time", title=f"Achievement timeline for {game_name}")
            return dcc.Graph(id='achievement-chart-figure', figure=fig)
        
    # if nothing was returned before this, return an empty graph
    fig = go.Figure()
    fig.update_layout(title="No achievements found")
    return dcc.Graph(id='achievement-chart-figure', figure=fig)
