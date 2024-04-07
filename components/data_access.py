import pandas as pd

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

# get_data_apart_sub(datasets)
#   get_data will read the needed data out of the CSV-files and put these in a pandas dataframe.
#
#   params:     datasets:               Array of dataset names.
#   returns:    categories_data:        DataFrame
#               cleaned_data:           DataFrame
#               full_audio_data:        DataFrame
#               genres_data:            DataFrame
#               supported_audio_data:   DataFrame
def get_data_apart_sub(datasets):
    output =  []

    for dataset in datasets:
        tmp = get_data_specific(dataset)

        output.append(tmp)
    
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
# get_data_together_sub(datasets)
#   get_data_sub will read given data.
#
#   params:     datasets:   Array of datasets.
#   returns:    output:     DataFrame
def get_data_together_sub(datasets):
    tobe_merged = get_data_apart_sub(datasets)
     
    output = pd.concat(tobe_merged, axis=0)

    return output
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

get_data_apart_sub()