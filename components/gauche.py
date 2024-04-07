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
    
# get_data_specific(specific)
#   get_data_specific will read the data for one specific dataset.
#
#   params:     specific:   Name of the specific dataset tob red out.      
#   returns:    output:     DataFrame
def get_data_specific(specific):
    data_path = "./Data/"

    if specific == "categories":
        path = f"{data_path}categories.csv"
    elif specific == "cleaned":
        path = f"{data_path}cleaned_games.csv"
    elif specific == "full_audio":
        path = f"{data_path}full_audio_languages.csv"
    elif specific == "genres":
        path = f"{data_path}genres.csv"
    elif specific == "supported_audio":
        path = f"{data_path}supported_languages.csv"

    output = pd.read_csv(path)

    return output

# get_data_apart()
#   get_data will read the needed data out of the CSV-files and put these in a pandas dataframe.
#
#   params:     /
#   returns:    categories_data:        DataFrame
#               cleaned_data:           DataFrame
#               full_audio_data:        DataFrame
#               genres_data:            DataFrame
#               supported_audio_data:   DataFrame
def get_data_apart():
    all_datasets = ["categories", "cleaned", "full_audio", "genres", "supported_audio"]

    categories_data = get_data_specific(all_datasets[0])
    cleaned_data = get_data_specific(all_datasets[1])
    full_audio_data = get_data_specific(all_datasets[2])
    genres_data = get_data_specific(all_datasets[3])
    supported_audio_data  = get_data_specific(all_datasets[4])

    return categories_data, cleaned_data, full_audio_data, genres_data, supported_audio_data
# get_data_together()
#   get_data will read the needed data out of the CSV-files and put these in a pandas dataframe.
#
#   params:     /
#   returns:    output: DataFrame
def get_data_together():
    categories_data, cleaned_data, full_audio_data, genres_data, supported_audio_data = get_data_apart()
    tobe_merged = [categories_data, cleaned_data, full_audio_data, genres_data, supported_audio_data]

    output = pd.concat(tobe_merged, axis=0)

    return output