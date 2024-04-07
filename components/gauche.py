import sys

sys.path.append('/utils/')

import data_access
import plotly.graph_objects as go
import pandas as pd

# decide_colour(value)
#   decide_colour will change the colour of the gauche depending on the actual value.
#
#   params: value:  The value tobe displayed
#   return: String.
def decide_colour(value):
    if value < 50:
        return "Red"
    elif (value >= 50) and (value < 60):
        return "Orange"
    else:
        return "Green"

# gauche(value)
#   gauche will create a gauche depeninding on the percentage given to the plot.
#
#   params: value:   a percentual value that has to be shown.
#   returns: /
def gauche(value):
    x=  [0, 1]
    y = [0, 1]

    d = {'x': x, 'y': y}
    gauge = {'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': decide_colour(value)}, 'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [{'range': [0, value], 'color': 'lightblue'}, {'range': [value, 100], 'color': 'lightgray'}],
            'shape': "angular"}
    number = {'font': {'size': 100, 'color': decide_colour(value)}, 'suffix': "%"}

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain= d,
        gauge= gauge,
        number=number
    ))

    fig.update_layout(height=400)

    fig.show()

get_data_apart()