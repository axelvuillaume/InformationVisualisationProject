from dash import dcc
from dash import html

from components.top_games_chart import generate_top_games_chart
from components.hexagon import hexagone

def generate_home_layout(cleaned_games, categories, genres, supported_languages, full_audio_languages):
    return html.Div(
        id='main-canva',
        children=[
            html.H1('STEAM DASHBOARD'),
            html.Div(
                className="component-container",
                children=[
                    generate_top_games_chart(cleaned_games, n=10)
                ]
            ),
            html.Div(
                className="component-container",
                children=[
                    hexagone(categories, genres, n=9)
                ]
            )
        ]
    )
