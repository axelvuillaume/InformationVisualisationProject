from dash import html,  Input, Output, callback, callback_context
import dash_bootstrap_components as dbc

# alert_box()
#   alert_box will create the button & the alert box component needed in order to give extra information about the
#   graph.
#
#   params:     /
#   returns:    [button, alert]:    An array exisisting out of the button & alert with extra information.
def alert_box():
    button = dbc.Button("Show Alert", id="alert-toggle", n_clicks=0)
    alert = dbc.Alert([html.H4("Well done!", className="alert-heading"),
                              html.P("This is a more detailed alert with some additional content and custom styling."),
                              html.Hr(),
                              html.P("Add any HTML element here, like ", className="mb-0"),
                              html.A("Dash Documentation", href="https://dash.plotly.com", target="_blank")
                             ],
                      id="alert",
                      is_open=False,
                      dismissable=True,
                      color="success"
                     )

    return [button, alert]