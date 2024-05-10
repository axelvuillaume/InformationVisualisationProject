from dash import html, callback
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

def alert(unique_id):
    button_id = "0-toggle"
    alert_id = "0-alert"
    # button_id = f"{unique_id}-toggle"
    # alert_id = f"{unique_id}-alert"
    button_label = "?"
    alert_message = get_message(unique_id)

    button = dbc.Button(button_label, id=button_id, n_clicks=0, color="info")
    alert = dbc.Alert(alert_message, id=alert_id, is_open=False, dismissable=True, color="info")

    layout = html.Div([button,alert])

    @callback(Output(alert_id, "is_open"),
              Input(button_id, "n_clicks"),
              State(alert_id, "is_open")
              )
    def toggle_alert(n_clicks, is_open):
        print(is_open)
        return n_clicks >= 0


    return layout

def get_message(id):
    message = graph_dict.get(id)

    return message