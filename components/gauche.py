import data_access as da
import plotly.graph_objects as go
import pandas as pd

# foo(column):
# foo will get the needed data out of the cleanded_games CSV and analyse this for percentages.
#
#   params:     columns:    The numeric column to be analysed.
#   returns:    /
def foo(column):
    data = da.get_data_specific("cleaned")
    
    output = data.groupby(column).sum()

    return output

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

print(foo("price"))