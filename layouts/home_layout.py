from dash import dcc
from dash import html

from components.top_games_chart import generate_top_games_chart

def generate_home_layout(data):
    return html.Div(
        id='main-canva',
        children=[
            html.H1('STEAM DASHBOARD'),
            html.Div(
                className="component-container",
                children=[
                    generate_top_games_chart(data, n=10)
                ]
            ),
            html.Div(
                className="component-container",
                children=[
                    generate_top_games_chart(data, n=10)
                ]
            )
        ]
    )
