from dash import dcc, html, Input, Output, callback, State

from utils.load_data import categories, genres, current_user

def steam_id_component():
    return html.Div(children=[
        dcc.Store(id='steam-id-store'),
        
        html.Img(id='avatar', 
                 src='https://upload.wikimedia.org/wikipedia/commons/8/83/Steam_icon_logo.svg', 
                 style={'width': '100px', 'display': 'inline-block'}),

        html.Div([
            html.H2(
                id = 'user-title',
                style={'color': 'white'},
                children=[]
            ),
        
            html.Div([
                "Steam Id: ",
                dcc.Input(id='steam-id', placeholder="Insert Steam Id", value=current_user.steamid),
                html.Button(id='submit-steamid', n_clicks=0, children='Submit')
            ], style={'color': 'white', 'display': 'inline-block', 'margin-left': '1em'}),
        ]),
        
        html.Div(
            [
                dcc.Link('Home', href='/home', id='home-link', className='button', style={'margin-right': '0.5em'}),
                dcc.Link('Profile', href='/profile', id='profile-link', className='button', style={'margin-right': '0.5em'}),
                dcc.Link('Recommender', href='/recommender', id='recommender-link', className='button'),
            ], className='button-container wrapperP_one',
        ),
    ], 
    style={
        'display': 'flex', 
        'flex-direction': 'row', 
        'justify-content': 'space-between', 
        'align-items': 'center',
        'padding': '1em',
        'box-shadow': '0.3em 0.3em 0.1em 0.5em rgb(18, 18, 18)',
        'margin-bottom': '1em',
        # 'border-bottom': '1px solid grey',
    })

@callback(Output('steam-id-store', 'data', allow_duplicate=True),
          Input("submit-steamid", "n_clicks"),
          State("steam-id", "value"),
          running=[(Output("submit-steamid", "disabled"), True, False)],
          prevent_initial_call=True
          #While callback is running -> button property disabled = True; when done, disabled = False
         )
def update_current_user(_, steamid):
    current_user.steamid = steamid
    return steamid

@callback(Output('user-title', "children"),
          Input('steam-id-store', 'data')
         )
def user_title_message(_):
    return f"Welcome back, {current_user.displayname}!"

@callback(Output('avatar', "src"),
          Input('steam-id-store', 'data')
         )
def user_title_message(_):
    return current_user.avatar
