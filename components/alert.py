from dash import html, callback, MATCH
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc

graph_dict = {0: "A bar  chart given the Top 10 games based on average playtime.\nx-axis:\tGame titles\ny-axis:\tAverage play time in Minutes",
              1: "A gauge given the percentage of positive review for the top 3 languages.",
              2: "A sunburst graph showing the most popular categories of game according to average playtime. \nClick on an area to see composition.",
              3: "Geographic map showing how many games are supported for a given language.\nThe bluer the colour the more games there are.",
              4: "Spider graph showing amount of games and playtime per genre or category in comparison with the chosen friend.\n You can select a specific category or genre by clicking on the labels on the spider graph in order to compare the games and playtime of the selected genre or category with the selected friend.",
              5: "This bubble chart presents five recommended games to buy based on the players' most played genres. These games are selected using a custom score that factors in key aspects often considered important in video games, such as the number of positive reviews and overall popularity (total number of reviews). Each bubble's color represents a different genre, while the bubble's size reflects the total number of reviews for that game. Hover over the bubbles to see detailed information. You can select or deselect genres in the legend, or double-click to focus on a specific genre. Double-click on the chart to reset it. To filter games by price range, simply drag across the graph.",
              6: "Stacked Barchart showing the playtime in hours for games in the user's steam library, each bar shows games within a certain genre. "
              + "Use the slider to change the amount of games shown. "
              + "Games appear in order of least to most playtime, which means bigger blocks start showing up on top as you increase the amount of games shown."
              + "Clicking on a game results in an updated 'genre playtime' graph (right) and 'achievement timeline' graph (below), if they are available. You can select and deselect genres in the legend, or isolate one genre by double clicking on it. " 
              + "To restore the graph to it's original state, double click somewhere on the graph. Alternately you can drag across the graph to view a zoomed in selection. The same actions can be done on the achievement chart. "
              + "Hover over items to view the full details.",
              7: "linechart text"
             }

@callback(Output({'type': 'alert_message', 'alert-id': MATCH}, "is_open"),
          Input({'type': 'alert_button', 'alert-id': MATCH}, "n_clicks"),
          State({'type': 'alert_message', 'alert-id': MATCH}, 'is_open'),
          prevent_initial_call=True,
         )
def toggle_alert(_, is_open):
    return not is_open #return opposite of current is_open state

@callback(Output({'type': 'alert_button', 'alert-id': MATCH}, "style"),
          Input({'type': 'alert_message', 'alert-id': MATCH}, "is_open")
         )
def toggle_button_hide(is_open):
    return {'display':'none'} if is_open else {'display':'block'} # if alert message is open, hide the button

def alert(unique_id):
    alert_id = f"{unique_id}-alert"
    button_label = "?"
    alert_message = get_message(unique_id)

    layout = html.Div([dbc.Button(button_label, id={"type" : "alert_button", "alert-id": alert_id},
                                  n_clicks=0,
                                  className=f"mb-1 alert-button{unique_id}"),
                       dbc.Alert(alert_message,
                                 id={"type" : "alert_message", "alert-id": alert_id},
                                 is_open=False,
                                 dismissable=True)
                       ])

    return layout

def get_message(id):
    message = graph_dict.get(id)

    return message
