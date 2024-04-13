from dash import dcc
import plotly.graph_objects as go
import pandas as pd

import utils.data_processing as dp

# foo(column):
# foo will get the needed data out of the cleanded_games CSV and analyse this for percentages.
# TODO: rename to more descriptive name
#
#   params:     columns:    The numeric column to be analysed.
#   returns:    /
def foo(column, per_thing, plot):
    output = []
    column_1 = dp.translate_column_dataset(per_thing)
    
    if column_1 == "cleaned":
        data = dp.get_data_specific(column_1)
    else:
        datasets = ["cleaned", column_1]

        data  = dp.get_data_together_sub(datasets)
    
    grouped = data.groupby(per_thing).sum()
    grouped = grouped.sort.head(10)
    total = data[column].sum()
    
    grouped_by_1 =  grouped[column]
    grouped_by_2 = data[per_thing].unique()
    t = 0
    
    for thing in grouped_by_2:
        go = isinstance(thing, str)

        if go:
            val = grouped_by_1[thing]
            per = (val / total) * 100
            t += per

            print(f"\t{thing}:\t{val}\t<=>\t{per}")
            if plot:
                output.append(gauche(per))
            else:
                print("foo")

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

    return dcc.Graph(id='top-games-chart', figure=fig)

# foo("price", "categories", False)