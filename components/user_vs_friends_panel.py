from dash import Dash, dcc, html, Input, Output, callback, State

from components.hexagon import hexagon_old, hexagon_generic
from utils.data_processing import get_n_best_gen_or_cat_by_hours, get_all_gen_or_cat, get_game_list_from_api, get_all_gen_or_cat_by_hours
from utils.load_data import categories, genres, current_user
from utils.classes.steam_user import Steam_User

current_friend_UVFcompo = None

def generate_user_vs_friends_panel():
    return html.Div(
        children=[
            dcc.Store(id='current-friend-id-store'), 
            html.Div(
                children=[
                    html.Div(
                        id='hexagon-menu',
                        children=[
                            html.H4("Number of sides:", style={'color': 'white','padding-left': '0.5em','padding-right': '0.5em'}),
                            dcc.Dropdown(
                                id='side-selector',
                                options=[
                                    {'label': str(i), 'value': i} for i in range(5, 10)
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
                    html.Div("Loading...", id='hexagonuser', style={'color': 'white'})
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
                    html.Div("Loading...", id='hexagonfriend', style={'color': 'white'})
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
    if (games is None or games.empty) :
        return html.Div("No data available for this user", style={'color': 'white'})

    data_to_use = genres if(category_select == 'genres') else categories

    ranking = {}
    playtime_by_gen_or_cat = get_n_best_gen_or_cat_by_hours(games, data_to_use, n)
    count_by_gen_or_cat = get_all_gen_or_cat(games, data_to_use)
    for key in playtime_by_gen_or_cat.keys():
        ranking[key] = [int(playtime_by_gen_or_cat.get(key,0)/60), count_by_gen_or_cat.get(key,0)]

    ranking_pairs = sorted(ranking.items())  #Sort by keys
    ranking = dict(ranking_pairs)

    colors = ['#1b3b80', '#1999ff']
    names = ['Playtime', 'Count']

    return hexagon_generic(ranking, colors, names)

@callback(
    Output('hexagonfriend', "children"),
    [Input('steam-id-store', 'data'),
     Input('current-friend-id-store', 'data'),
     Input('side-selector', 'value'),
     Input('chart-type', 'value')]
)
def compute_hexagon_friend(_,__, n, category_select):

    if(current_friend_UVFcompo is None):
        return html.Div("No friends", style={'color': 'white'})
    else:
        friendgames = current_friend_UVFcompo.games
    if (friendgames is None or friendgames.empty):
        return html.Div("No data available for this user", style={'color': 'white'})

    data_to_use = genres if(category_select == 'genres') else categories

    playtime_by_gen_or_cat_all = get_all_gen_or_cat_by_hours(friendgames, data_to_use)
    playtime_by_gen_or_cat = {}
    for key in get_n_best_gen_or_cat_by_hours(current_user.games, data_to_use, n).keys():
        playtime_by_gen_or_cat[key] = playtime_by_gen_or_cat_all.get(key,0)


    count_by_gen_or_cat = get_all_gen_or_cat(friendgames, data_to_use)
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
    [Input('steam-id-store', 'data')]
)
def set_friend_selector(_):
    if (current_user.friends is None or current_user.friends.empty):
        return [], None, {'width': 'auto', 'align-self': 'center', 'padding-left': '0.5em', 'padding-right': '0.5em'}

    options = [{'label': f"{index+1}. {row['displayname']}", 'value': row['steamid']} for index, row in current_user.friends.iterrows()]
    default_value = current_user.friends.iloc[0]['steamid']
    max_option_length = max(len(option['label']) for option in options)
    dropdown_width = max_option_length * 11

    return options, default_value, {'width': dropdown_width ,'align-self': 'center', 'padding-left': '0.5em', 'padding-right': '0.5em'}

@callback(
    Output('current-friend-id-store', 'data'),
    Input('friend-selector', "value")
)
def update_current_friend(friend_id):
    global current_friend_UVFcompo
    if(current_friend_UVFcompo is None and friend_id is not None):
        current_friend_UVFcompo = Steam_User(friend_id, fetch_friends=False)
    elif(current_friend_UVFcompo is not None and friend_id is not None):
        current_friend_UVFcompo.steamid = friend_id
    else:
        current_friend_UVFcompo = None

    return friend_id

#def compute_hexagon(_, n, category_select):
#    return hexagon(categories, genres, category_select=category_select, n=n)