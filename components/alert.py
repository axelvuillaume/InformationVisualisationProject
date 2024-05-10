from dash import html, callback
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc

def alert(unique_id, alert_message="Hello! I am an alert!"):
    button_id = f"{unique_id}-toggle"
    alert_id = f"{unique_id}-alert"
    button_label = "?"

    layout = html.Div([dbc.Button(button_label, id=button_id, n_clicks=0),
                       dbc.Alert(alert_message, id=alert_id, is_open=False, dismissable=True)
                       ])

    @callback(Output(alert_id, "is_open"),
                  [Input(button_id, "n_clicks")],
                  [State(alert_id, "is_open")]
                 )
    def toggle_alert(n_clicks, is_open):
        return not n_clicks == 0

    return layout