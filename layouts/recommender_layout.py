from dash import dcc, html, Input, Output, callback, State
from components.steam_id import steam_id_component
from components.user_vs_friends_panel import generate_user_vs_friends_panel
from components.bubble_chart import bubble_chart
from components.alert import alert

from utils.load_data import current_user

def generate_recommender_layout():
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

            html.Div(
                className="component-container wrapperP_three",
                id='user_vs_friends_panel',
                children=[alert(4),
                          generate_user_vs_friends_panel()
                         ]
            ),

            html.Div(
                className="component-container wrapperP_four",
                id = 'bubble-chart',
                children=[#bubble(n=8)
                         ]
            ),
        ],
    )
    
# Note: Most callbacks are activated once steam-id-store is changed, 
# this is a dcc.Store component in the steam_id.py file (which is updated everytime the user submits a new steamid)

@callback(
    Output('bubble-chart', "children"),
    Input('steam-id-store', 'data')
)
def bubble(_):
    return bubble_chart()
