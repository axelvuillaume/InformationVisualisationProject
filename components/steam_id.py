from dash import Dash, dcc, html, Input, Output, callback, State

from components.hexagon import hexagon_old, hexagon_generic
from utils.data_processing import get_n_best_gen_or_cat_by_hours, get_all_gen_or_cat, get_game_list_from_api, get_all_gen_or_cat_by_hours
from utils.load_data import categories, genres, current_user
from utils.classes.steam_user import Steam_User

def steam_id_component():
    return html.Div(children=[
        dcc.Store(id='steam-id-store'),
        
        html.Img(id='avatar', 
                 src='https://upload.wikimedia.org/wikipedia/commons/8/83/Steam_icon_logo.svg', 
                 style={'width': '100px', 'display': 'inline-block'}),

        html.H2(
            id = 'user-title',
            style={'color': 'white'},
            children=[]
        ),
        
        html.Div([
            "Steam Id: ",
            dcc.Input(id='steam-id', placeholder="Insert Steam Id", value='76561198150561997'),
            html.Button(id='submit-steamid', n_clicks=0, children='Submit')
        ], style={'color': 'white', 'display': 'inline-block', 'margin-left': '1em'}),
    ], 
    style={
        'display': 'flex', 
        'flex-direction': 'row', 
        'justify-content': 'space-around', 
        'align-items': 'center',
        'padding': '1em',
        'box-shadow': '0.3em 0.3em 0.1em 0.5em rgb(18, 18, 18)'
        # 'border-bottom': '1px solid grey',
    })

    

@callback(
    Output('user-title', "children"),
    Input('steam-id-store', 'data')
)
def user_title_message(_):
    return f"Welcome back, {current_user.displayname}!"

@callback(
    Output('avatar', "src"),
    Input('steam-id-store', 'data')
)
def user_title_message(_):
    return current_user.avatar