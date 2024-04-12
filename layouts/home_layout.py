from dash import Dash, dcc, html, Input, Output, callback

from components.top_games_chart import generate_top_games_chart
from components.hexagon import hexagon
from Data.load_data import cleaned_games, categories, genres, supported_languages, full_audio_languages


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
            )
        ]
    )

@callback(
    Output('hexagon', "children"),
    Input("steam-id", "value"),
)
def compute_hexagon(steam_id):
    print(hexagon(categories, genres, steam_id, n=8))
    return hexagon(categories, genres, steam_id, n=8)
