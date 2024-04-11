import pandas as pd

all_datasets = ["categories", "cleaned", "full_audio", "genres", "supported_audio"]

def load_data(file_path):
    return pd.read_csv(file_path)

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

    output = load_data(path)

    return output

# get_data_apart_sub(datasets)
#   get_data will read the needed data out of the CSV-files and put these in a pandas dataframe.
#
#   params:     datasets:   Array of dataset names.
#   returns:    output:     Array of dataframes.            
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
    dataframes = get_data_apart_sub(all_datasets)

    categories_data = dataframes[0]
    cleaned_data = dataframes[1]
    full_audio_data = dataframes[2]
    genres_data = dataframes[3]
    supported_audio_data = dataframes[4]

    return categories_data, cleaned_data, full_audio_data, genres_data, supported_audio_data

# get_data_together_sub(datasets)
#   get_data_sub will read given data.
#
#   params:     datasets:   Array of datasets.
#   returns:    output:     DataFrame
def get_data_together_sub(datasets):
    tobe_merged = get_data_apart_sub(datasets)
     
    output = pd.concat(tobe_merged, axis=1)

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

# group_by_column(column, per_thing)
#   group_by_column will give the percentages of the "column" value per "per_thing" values.
#
#   params:     columns:    The numeric column to be analysed.
#               per_thing:  per whichch column there have to be grouped.
#   returns:    /
def group_by_column(column, per_thing):
    percentages = []
    new_name = f"{column}_{per_thing}"

    if per_thing == "cleaned":
        data = get_data_specific(per_thing)
    else:
        datasets = ["cleaned", per_thing]

        data  = get_data_together_sub(datasets)
    
    grouped = data.groupby(per_thing).sum()
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

            percentages.append(per)
    
    df = get_data_specific(per_thing)
    df[new_name] = percentages

    print(df.head(5))

group_by_column("price", "categories")