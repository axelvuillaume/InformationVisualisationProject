from dash import html, callback, MATCH
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc

graph_dict = {0: "A bar  chart given the Top 10 games based on average playtime.\nx-axis:\tGame titles\ny-axis:\tAverage play time in Minutes",
              1: "A gauge given the percentage of positive review for the top 3 languages.",
              2: "A sunburst graph showing distribution of average playtime\nClick on an area to see composition.",
              3: "Geographic map showing how many games are supported for a given language.\nThe bluer the colour the more games there are.",
              4: "Spider graph showing amount of games per genre or category in comparison with the chosen friend",
              5: "A bubble chart showing the the players most positive genres size indicate the amount of reviews.\nx-axis:\tPrice\ny-axis:\tPercentage of the reviews that are positive.\nColour:\tGenre\nSize:\tTotal amount of reviews.",
              6: "Barchart showing the playtime in hours for the amount of genres shown.\nUse the slide beneath to change the amount of games or amount of genres shown."
             }

@callback(
    Output({'type': 'alert_message', 'alert-id': MATCH}, "is_open"),
    Input({'type': 'alert_button', 'alert-id': MATCH}, "n_clicks"),
    State({'type': 'alert_message', 'alert-id': MATCH}, 'is_open'),
    prevent_initial_call=True,
)
def toggle_alert(_, is_open):
    return not is_open #return opposite of current is_open state

@callback(
    Output({'type': 'alert_button', 'alert-id': MATCH}, "style"),
    Input({'type': 'alert_message', 'alert-id': MATCH}, "is_open")
)
def toggle_button_hide(is_open):
    return {'display':'none'} if is_open else {'display':'block'} # if alert message is open, hide the button

def alert(unique_id):
    alert_id = f"{unique_id}-alert"
    button_label = "?"
    alert_message = get_message(unique_id)

    layout = html.Div([dbc.Button(button_label, id={"type" : "alert_button", "alert-id": alert_id}, n_clicks=0, className="mb-1"),
                       dbc.Alert(alert_message, id={"type" : "alert_message", "alert-id": alert_id}, is_open=False, dismissable=True)
                       ])

    return layout

def get_message(id):
    message = graph_dict.get(id)

    return message