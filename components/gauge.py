from dash import dcc
import plotly.graph_objects as go

from utils import data_processing as dp

# gauge_percentages(column, per_thing):
#   gauge_percentages will get the needed data out of the cleanded_games CSV and analyse this for percentages.
#
#   params:     columns:    The numeric column to be analysed.
#               per_thing:  The element there should be grouped by.
#   returns:    /
def gauge_percentages(column, per_thing):
    try:
        output = []
        new_column = f"{column}%"
        
        df = dp.get_percentages(column, per_thing).sort_values(by=new_column, ascending=False)
        top = df.head(3)

        names = top[per_thing].to_numpy()
        values = top[new_column].to_numpy()

        
        for i in range(0, len(names)):
            name = f"{names[i]} vs. {column}"
            value = values[i]

            output.append(gauge(value, name))
        
        return output
    except Exception as e:
            print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- gauge_percentages:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")

# decide_colour(value)
#   decide_colour will change the colour of the gauche depending on the actual value.
#
#   params: value:  The value tobe displayed
#   return: String.
def decide_colour(value):
    # if value < 50:
    #     return "White"
    # elif (value >= 50) and (value < 60):
    #     return "Grey"
    # else:
    #     return "Black"

    return "Black"

# gauge(value, name)
#   gauge will create a gauge depeninding on the percentage given to the plot.
#
#   params:     value:  A percentual value that has to be shown.
#               name:   The name of the plot
#   returns:    /
def gauge(value, name):
    try:
        x=  [0, 1]
        y = [0, 1]

        d = {'x': x, 'y': y}
        gauge = {'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': decide_colour(value)}, 'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [{'range': [0, value], 'color': 'lightblue'}, {'range': [value, 100], 'color': 'lightgray'}],
                'shape': "angular"}
        number = {'font': {'size': 45, 'color': decide_colour(value)}, 'suffix': "%"}

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            domain= d,
            gauge= gauge,
            number=number,
            title=name
        ))

        return dcc.Graph(id='top-games-chart', figure=fig)
    except Exception as e:
            print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- gauge:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")
