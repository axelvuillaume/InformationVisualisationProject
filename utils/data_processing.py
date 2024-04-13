import pandas as pd

all_datasets = ["categories", "cleaned", "full_audio", "genres", "supported_audio"]

# get_file_name_group_by(per_thing)
#   get_file_name_group_by will generate a file name for the grouped_by CSV-files.
#
#   params:     per_thing:  Variant name for CSV-file.
#   returns:    output:     Path name of CSV-file.
def get_file_name(per_thing):
    output = f"./Data/{per_thing}_grouped_by.csv"

    return output

# load_data(file_path)
#   load_data will read a CSV file on the given path.
# 
#   params:     file_path:  The path to the tobe red CSV-file.
#   returns:    DataFrame.
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- load_data:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")

# write_data(dataframe, file_path)
#   write_data will write the given dataframe to a CSV-file stored on the given path.
#
#   params:     dataframe:  Dataframe to be save to an CSV-file
#               file_path:  The path where the dataframe has to be written.
#   returns:    /
def write_data(dataframe, file_path):
    try:
        dataframe.to_csv(file_path)
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- write_data:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")
# translate_column_dataset(column):
#   This dataset translate the name of a column into the name of the correct dataset where it can be found.
#
#   params:     column: Name of the column.
#   returns:    output: Name of dataset where column is to be found.
def translate_column_dataset(column):
    try:
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
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- translate_column_dataset:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")

# get_data_specific(specific)
#   get_data_specific will read the data for one specific dataset.
#
#   params:     specific:   Name of the specific dataset tob red out.      
#   returns:    output:     DataFrame
def get_data_specific(specific):
    try:
        specific =  translate_column_dataset(specific)
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
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- get_data_specific:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")

# get_data_apart_sub(datasets)
#   get_data will read the needed data out of the CSV-files and put these in a pandas dataframe.
#
#   params:     datasets:   Array of dataset names.
#   returns:    output:     Array of dataframes.            
def get_data_apart_sub(datasets):
    try:
        output =  []

        for dataset in datasets:
            tmp = get_data_specific(dataset)

            output.append(tmp)
        
        return output
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- get_data_apart_sub:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")
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
    try:
        dataframes = get_data_apart_sub(all_datasets)

        categories_data = dataframes[0]
        cleaned_data = dataframes[1]
        full_audio_data = dataframes[2]
        genres_data = dataframes[3]
        supported_audio_data = dataframes[4]

        return categories_data, cleaned_data, full_audio_data, genres_data, supported_audio_data
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- get_data_apart:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")

# get_data_together_sub(datasets)
#   get_data_sub will read given data.
#
#   params:     datasets:   Array of datasets.
#   returns:    output:     DataFrame
def get_data_together_sub(datasets):
    try:
        tobe_merged = get_data_apart_sub(datasets)
        
        output = pd.concat(tobe_merged, axis=1)

        return output
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- get_data_together_sub:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")
# get_data_together()
#   get_data will read the needed data out of the CSV-files and put these in a pandas dataframe.
#
#   params:     /
#   returns:    output: DataFrame
def get_data_together():
    try:
        categories_data, cleaned_data, full_audio_data, genres_data, supported_audio_data = get_data_apart()
        tobe_merged = [categories_data, cleaned_data, full_audio_data, genres_data, supported_audio_data]

        output = pd.concat(tobe_merged, axis=0)

        return output
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- get_data_together:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")

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
    try:
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
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- group_by_column:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")
# group_by_column_all_numerics(columns, per_thing)
#   group_by_column will give the percentages of the "columns" values per "per_thing" values.
#
#   params:     columns:    An array of column numeric columns.
#               per_thing:  per whichch column there have to be grouped.
#   returns:    /
def group_by_column_all_numerics(columns, per_thing):
    try:
        if per_thing == "cleaned":
            data = get_data_specific(per_thing)
        else:
            datasets = ["cleaned", per_thing]

            data  = get_data_together_sub(datasets)
        
        grouped = data.groupby(per_thing).sum()

        d = {}

        for column in columns:
            new_name = f"{column}%"
            print(f"\tBusy with:\t{new_name}")

            f = group_by_column(data, grouped, column, per_thing, new_name)

            print(f)

            d.update(f)

        df = pd.DataFrame(d)

        return df
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- group_by_column_all_numerics:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")

# make_percentage_files(columns, per_thing)
#   make-percentage_files will loop through the per_things array and make a new CSV file containing percentages of that per_thing.
#
#   params:     columns:    An array of  numeric columns.
#               per_things: An array of columns on what should be grouped by.
#   returns:    /
def make_percentage_files(columns, per_things):
    try:
        for per_thing in per_things:
            if not is_done[per_thing]:
                print(f"Dealing with\t{per_thing}")

                path = get_file_name(per_thing)

                df = group_by_column_all_numerics(columns, per_thing)

                print(df)

                write_data(df, path)

                print(f"Done with\t{per_thing}")
            else:
                print(f"{per_thing}\t\tis already translatted into a CSV-file.")
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- make_percentage_files:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")



columns = ["price", "dlc_count", "positive", "negative", "average_playtime_forever", "median_playtime_forever", "peak_ccu", "min_owners", "max_owners"]
per_things = ["categories", "full_audio_languages", "genres", "supported_languages"]

is_done = {"categories": True, "full_audio_languages": False, "genres": False, "supported_languages": False} # Please change the truth-statement as needed.

# make_percentage_files(columns, per_things)