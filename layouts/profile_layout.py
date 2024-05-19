from dash import dcc, html, Input, Output, callback, State
from components.steam_id import steam_id_component
from components.user_playtime_bar_chart import playtime_per_genre, playtime_games_per_genre
from components.slider import steam_game_slider
from components.achievement_chart import achievement_chart

from utils.load_data import current_user

def generate_profile_layout():
    return html.Div(
        className ="profile_wrapper",
        id='main-canva',
        style={'padding': '1em', 'box-sizing':'border-box'},
        children=[
            html.Div(
                className="component-container wrapperP_two",
                id='',
                children=[
                    steam_id_component(),
                ]
            ),

            #html.Div(
            #    className="component-container wrapperP_two",
            #    id='',
            #    children=[
            #        steam_id_component(),
            #    ]
            #),

            html.Div(
                className="component-container wrapperP_five",
                id = 'user-playtime-chart',
                children=[
                    html.Div(
                        id = 'user-playtime-chart',
                    ),
                    html.Div(
                        style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'flex-start', 'align-items': 'center'},
                        children=[
                            html.H5("Game Amount: ", style={'color': 'white'}),
                            html.Div(
                                id = 'user-game-slider',
                                style={'width': '80%', 'margin-top': '1em'}
                            )
                        ]
                    ),
               ],
            ),

            html.Div(
               className="component-container wrapperP_six",
               id = 'detail-playtime-chart',
               children=[
                   
               ],
                #scrollbar functionality but with fixed height
                #style={'overflowY': 'scroll', 'height': '100vh'}
            ),

            html.Div(
               className="component-container  wrapperP_seven",
               id = 'achievement_timeline_chart',
               children=[
                   achievement_chart(None, None)
               ],
            ),
        ],
    )
    
# Note: Most callbacks are activated once steam-id-store is changed, 
# this is a dcc.Store component in the steam_id.py file (which is updated everytime the user submits a new steamid)

@callback(
    Output('user-playtime-chart', "children"),
    Input('steam-id-store', 'data'),
    Input("user-playtime-slider", "value"),
)
def playtime_chart(_, games_slider_value):
    return playtime_per_genre(games_amount=games_slider_value)

@callback(
    Output('user-game-slider', "children"),
    Input('steam-id-store', 'data')
)
def playtime_slider(_):
    return steam_game_slider()

@callback(
    Output('detail-playtime-chart', 'children'),
    Input('playtime-bar-chart-figure', 'clickData'))
def display_click_data(clickData):
    # 'x' key of the clickData contains the genre name
    genre_name = clickData['points'][0]['x'] if clickData else None
    return playtime_games_per_genre(genre_name)

@callback(
    Output('achievement_timeline_chart', 'children'),
    Input('playtime-bar-chart-figure', 'clickData'))
def display_achievement_chart(clickData):
    game_id = clickData['points'][0]['customdata'][0] if clickData else None
    return achievement_chart(game_id, game_name=clickData['points'][0]['text'])
