from dash import dcc
from dash import html

from components.top_games_chart import generate_top_games_chart
from components.gauge import foo

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
            ),
            html.Div(
                className="component-container",
                children=[
                    html.Div(
                        className="component-container",
                            children=[foo("price", "categories")[0]]
                        ),
                    html.Div(
                        className="component-container",
                        children=[foo("price", "categories")[1]]
                        ),
                    html.Div(
                        className="component-container",
                        children=[foo("price", "categories")[2]]
                        ),
                ]
            )
        ]
    )
