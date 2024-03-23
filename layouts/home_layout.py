from dash import dcc
from dash import html

from components.top_games_chart import generate_top_games_chart

def generate_home_layout(data):
    return html.Div([
        html.H1('Game Recommendation Dashboard'),
        html.Div([
            generate_top_games_chart(data, n=10)
        ])
    ])
