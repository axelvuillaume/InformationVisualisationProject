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

# group_by_column(data, grouped_by, column, per_thing, new_name)
#   group_by_column will give the percentages of the "column" following the given groupe dataframe.
#
#   params:     data:       Dataframe with original data.
#               grouped_by: Dataframe grouped by certain column.
#               column:     Name of the numeric column.
#               per_thing:  Name of the column on which is grouped.
#               new_name:   The name of the new column.
#   returns:    DataFrame
def group_by_column(data, grouped_by, column, per_thing, new_name):
    percentages = []

    total = data[column].sum()
    
    grouped_by_1 =  grouped_by[column]
    grouped_by_2 = data[per_thing].unique()
    
    for thing in grouped_by_2:
        go = isinstance(thing, str)

        if go:
            val = grouped_by_1[thing]
            per = (val / total) * 100
            
            percentages.append(per)

    d = {per_thing: grouped_by_2, new_name: percentages}

    return d
# group_by_column_all_numerics(columns, per_thing)
#   group_by_column will give the percentages of the "columns" values per "per_thing" values.
#
#   params:     columns:    An array of column numeric columns.
#               per_thing:  per whichch column there have to be grouped.
#   returns:    /
def group_by_column_all_numerics(columns, per_thing):
    path = f"./Data/{per_thing}_grouped_by.csv"

    if per_thing == "cleaned":
        data = get_data_specific(per_thing)
    else:
        datasets = ["cleaned", per_thing]

        data  = get_data_together_sub(datasets)
    
    grouped = data.groupby(per_thing).sum()

    d = {}

    for column in columns:
        new_name = f"{column}%"
        print(f"Busy with:\t{new_name}")

        d.update(group_by_column(data, grouped, column, per_thing, new_name))

    df = pd.DataFrame(d)

    return df
columns = ["price", "dlc_count", "positive", "negative", "average_playtime_forever", "median_playtime_forever", "peak_ccu", "min_owners", "max_owners"]
per_thing = "categories"

print(group_by_column_all_numerics(columns, per_thing))