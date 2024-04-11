from dash import dcc
import plotly.graph_objects as go
import pandas as pd

import utils.data_processing as dp

# translate_column_dataset(column):
#   This dataset translate the name of a column into the name of the correct dataset where it can be found.
#
#   params:     column: Name of the column.
#   returns:    output: Name of dataset where column is to be found.
def translate_column_dataset(column):
    print(f"\tStart translating to dataset\t{column}")
    
    if column == "categories":
        output = "categories"
    elif column == "full_audio_languages" :
        output = "full_audio"
    elif column == "genres":
        output = "genres"
    elif column == "supported_languages":
        output = "supported_audio"
    else:
        output = "cleaned"

    print(f"\tDone with translation\t{column}")

    return output

# foo(column):
# foo will get the needed data out of the cleanded_games CSV and analyse this for percentages.
# TODO: rename to more descriptive name
#
#   params:     columns:    The numeric column to be analysed.
#   returns:    /
def foo(column, per_thing):
    output = []
    print(">>>Starting foo<<<")
    print("Translating column to a datastring")

    column_1 = translate_column_dataset(per_thing)
    print(f"Done translating: {column_1}")
    print("Getting datasets")
    if column_1 == "cleaned":
        print("dataset is in cleaned")
        data = dp.get_data_specific(column_1)
    else:
        print("dataset something else")
        datasets = ["cleaned", column_1]

        data  = dp.get_data_together_sub(datasets)
    print("Done getting datasets")
    print(f"Grouping on {per_thing}")
    grouped = data.groupby(per_thing).sum()
    grouped = grouped.sort.head(10)
    total = data[column].sum()
    print(f"Done with Grouping on {per_thing}")

    grouped_by_1 =  grouped[column]
    grouped_by_2 = data[per_thing].unique()
    t = 0
    print("Printing loop")
    for thing in grouped_by_2:
        go = isinstance(thing, str)

        if go:
            val = grouped_by_1[thing]
            per = (val / total) * 100
            t += per

            print(f"\t{thing}:\t{val}\t<=>\t{per}")
            output.append(gauche(per))
    print(f"Done printing loop\t{t}")

    print(">>>Done foo<<<")
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