import data_access as da
import plotly.graph_objects as go
import pandas as pd

# translate_column_dataset(column):
#   This dataset translate the name of a column into the name of the correct dataset where it can be found.
#
#   params:     column: Name of the column.
#   returns:    output: Name of dataset where column is to be found.
def translate_column_dataset(column):
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

    return output

# foo(column):
# foo will get the needed data out of the cleanded_games CSV and analyse this for percentages.
#
#   params:     columns:    The numeric column to be analysed.
#   returns:    /
def foo(column, per_thing):
    column_1 = translate_column_dataset(per_thing)

    if column_1 == "cleaned":
        data = da.get_data_specific(column_1)
    else:
        datasets = ["cleaned", column_1]

        data  = da.get_data_together_sub(datasets).sum()

    output = data.groupby(column_1).sum

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

print(foo("price", "categories")['price'].unique())