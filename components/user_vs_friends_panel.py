from dash import Dash, dcc, html, Input, Output, callback, State

from components.hexagon import hexagon_old, hexagon_generic
from utils.data_processing import get_n_best_gen_or_cat_by_hours, get_all_gen_or_cat
from utils.load_data import cleaned_games, categories, genres, current_user, supported_languages, full_audio_languages

def generate_user_vs_friends_panel():
    return html.Div(
        children=[
            html.Div(
                children=[
                    html.H2("My Profile", style={'color': 'white'}),
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
                    html.Div(id='hexagonuser')
                ],
                style={'display': 'flex', 'flex-direction': 'column','width': '25%'}
            ),
            html.Div(
                children=[
                    html.H2("Friends", style={'color': 'white'}),
                    html.Div(
                        id='friend-menu',
                        children=[
                            html.H4("Select friend:", style={'color': 'white','padding-left': '0.5em','padding-right': '0.5em'}),
                            dcc.Dropdown(
                                id='friend-selector',
                                    clearable=False,
                                    searchable=True,
                                    style={'width': 'auto','align-self': 'center','padding-left': '0.5em','padding-right': '0.5em'}
                            )
                        ],
                        style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between' , 'width': '400px','background-color': '#171D25'}
                    ),
                ],
                style={'display': 'flex', 'flex-direction': 'column','width': '25%'}
            )
        ],
        style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between'}
    )


@callback(
    Output('hexagonuser', "children"),
    [Input('steam-id-store', 'data'),
     Input('side-selector', 'value'),
     Input('chart-type', 'value')]
)
def compute_hexagon_user(_, n, category_select):

    games = current_user.games
    select = category_select

    if(select == 'genres'):
        data_to_use = genres
    if(select == 'categories'):
        data_to_use = categories
    else:
        data_to_use = genres

    playtime_by_gen_or_cat = get_n_best_gen_or_cat_by_hours(games, data_to_use, n)
    count_by_gen_or_cat = get_all_gen_or_cat(games, data_to_use)
    
    #Merge the two dictionaries
    ranking = {}
    for key in playtime_by_gen_or_cat.keys():
        ranking[key] = [int(playtime_by_gen_or_cat.get(key,0)/60), count_by_gen_or_cat.get(key,0)]

    ranking_pairs = sorted(ranking.items())  #Sort by keys
    ranking = dict(ranking_pairs)

    colors = ['#1b3b80', '#1999ff']
    names = ['Playtime', 'Count']

    return hexagon_generic(ranking, colors, names)

@callback(
    [Output('friend-selector', "options"),
    Output('friend-selector', "value"),
    Output('friend-selector', "style")],
    [Input('steam-id-store', 'data')],
)
def set_friend_selector(_):
    options = [{'label': f"{index+1}. {row['steamid']}", 'value': row['steamid']} for index, row in current_user.friends.iterrows()]
    default_value = current_user.friends.iloc[0]['steamid']
    max_option_length = max(len(option['label']) for option in options)
    dropdown_width = max_option_length * 11

    return options, default_value, {'width': dropdown_width ,'align-self': 'center', 'padding-left': '0.5em', 'padding-right': '0.5em'}

#def compute_hexagon(_, n, category_select):
#    return hexagon(categories, genres, category_select=category_select, n=n)