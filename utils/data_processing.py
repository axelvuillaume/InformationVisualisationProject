import pandas as pd
import requests

all_datasets = ["categories", "cleaned", "full_audio", "genres", "supported_audio"]
API_KEY = "E145AF167FA00841A4A2956EEEBEA929"

# get_file_name_group_by(per_thing)
#   get_file_name_group_by will generate a file name for the grouped_by CSV-files.
#
#   params:     per_thing:  Variant name for CSV-file.
#   returns:    output:     Path name of CSV-file.
def get_file_name(per_thing):
    output = f"./data/{per_thing}_grouped_by.csv"

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
# translate_column_group_by(per_thing):
#   This dataset translate the name of a column into the name of the correct dataset where it can be found.
#   This for the grouped_by CSV-files.
#
#   params:     per_thing:  The name of the column on what the CSV-file is grouped
#   returns:    output: Name of dataset where column is to be found.
def translate_column_group_by(per_thing):
    try:
        output = f"{per_thing}_grouped_by.csv"

        return output
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- translate_column_group_by:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")

# get_data_specific(specific)
#   get_data_specific will read the data for one specific dataset.
#
#   params:     specific:   Name of the specific dataset tob red out.      
#   returns:    output:     DataFrame
def get_data_specific(specific):
    try:
        specific =  translate_column_dataset(specific)
        data_path = "./data/"

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

# get_percentages(data, grouped_by, column, per_thing)
#   get_percentages will give the percentages of the "column" following the given groupe dataframe.
#
#   params:     data:       Dataframe with original data.
#               grouped_by: Dataframe grouped by certain column.
#               column:     Name of the numeric column.
#               per_thing:  Name of the column on which is grouped.
#   returns:    DataFrame
def get_percentages(column, per_thing):
    try:
        percentages = []
        path = f"./Data/{translate_column_group_by(per_thing)}"

        data = load_data(path)

        total = data[column].sum()
        
        grouped_by_1 =  data[column]
        grouped_by_2 = data[per_thing].unique()
        
        for i in range(0, len(grouped_by_1)):
            value = grouped_by_1[i]
            name = grouped_by_2[i]

            per = (value / total) * 100

            percentages.append(per)

        d = {per_thing: grouped_by_2, f"{column}%": percentages}
        
        output = pd.DataFrame(d)

        return output
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- get_percentages:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")

# group_by_per_thing(data, per_thing)
#   group_by_per_thing will give the percentages of the "columns" values per "per_thing" values.
#
#   params:     data:       The dataframe where the information will be red out.
#               per_thing:  per whichch column there have to be grouped.
#   returns:    grouped:    Dataframe of the grouped data.
def group_by_per_thing(data, per_thing):
    try:
        grouped = data.groupby(per_thing).sum()

        grouped[per_thing] = grouped.index

        return grouped
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- group_by_per_thing:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")

# group_by_all(per_thing)
#   group_by_all will give the percentages of the "columns" values per "per_thing" values.
#
#   params:     per_thing:  per whichch column there have to be grouped.
#   returns:    grouped:    Dataframe of the grouped data.
def group_by_all(per_thing):
    try:
        if per_thing == "cleaned":
            data = get_data_specific(per_thing)
        else:
            datasets = ["cleaned", per_thing]

            data  = get_data_together_sub(datasets)
        
        grouped = group_by_per_thing(data, per_thing)

        return grouped
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- group_by_all:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")

# make_file(columns, per_thing, is_done)
#   make-file will loop through the per_things array and make a new CSV file containing percentages of that per_thing.
#
#   params:     columns:    An array of  numeric columns.
#               per_things: An array of columns on what should be grouped by.
#               is_done:    An dictionary keeping wich datasets are already prepared and wich not.
#   returns:    /
def make_file(columns, per_things, is_done):
    try:
        for per_thing in per_things:
            if not is_done[per_thing]:
                print(f"Dealing with\t{per_thing}")

                path = get_file_name(per_thing)

                df = group_by_all(per_thing)[columns]

                write_data(df, path)

                print(f"Done with\t{per_thing}")
            else:
                print('{:<20} is already translated into a CSV-file'.format(per_thing)) #:<20 is used to left-align the first word
    except Exception as e:
        print(f"\t>>>>>>>>>><<<<<<<<<<\n\t\tAn exception ocurred -- make_file:\n\t\t{e}\n\t>>>>>>>>>><<<<<<<<<<")

def get_player_information_from_api(player_ids):
    player_info_list = []
    player_ids_chunks = [player_ids[i:i+100] for i in range(0, len(player_ids), 100)]
    for chunk in player_ids_chunks:
        api_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={API_KEY}&steamids={','.join(chunk)}&format=json"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                # example json output can be found here: https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={API_KEY}&steamids=76561198222609456&format=json
                data = response.json()
                players_info = data['response']['players']

                player_info_list.extend(players_info)
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    return player_info_list

def get_friends_list_from_api(player_id):
    print("Getting friends from API")
    api_url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={API_KEY}&steamid={player_id}&relationship=friend&format=json"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            friends = data['friendslist']['friends']
            friends_data = {'steamid': [], 'displayname': []}
            friends_ids = [friend['steamid'] for friend in friends]
            friends_displaynames = {friend['steamid']: friend['personaname'] for friend in get_player_information_from_api(friends_ids)}

            for friend in friends:
                friends_data['steamid'].append(friend['steamid'])
                friends_data['displayname'].append(friends_displaynames[friend['steamid']])

            friends_df = pd.DataFrame(friends_data)
            return friends_df
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_game_list_from_api(player_id):
    print("Getting games from API")
    api_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={player_id}&format=json"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            games = data['response']['games']
            games_data = {'app_id': [], 'playtime_forever': []}

            for game in games:
                games_data['app_id'].append(game['appid'])
                games_data['playtime_forever'].append(game['playtime_forever'])

            games_df = pd.DataFrame(games_data)
            return games_df
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_achievements_for_game(player_id, app_id):
    print(f"Getting achievements for {app_id} from API")
    api_url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={API_KEY}&steamid={player_id}&format=json&l=en"
    global_achievements_url = f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={app_id}&format=json"
    
    try:
        response = requests.get(api_url)
        response_global = requests.get(global_achievements_url)
        if response.status_code == 200 and response_global.status_code == 200:
            data = response.json()
            data_global = response_global.json()
            game_name = data['playerstats']['gameName']
            achievements = data['playerstats']['achievements']
            global_achievements = data_global['achievementpercentages']['achievements']
            return {'name': game_name, 'achievements': achievements, 'global_achievements': global_achievements}
        else:
            print(f"Error: {response.status_code} - {response.text}") if response.status_code != 200 else print(f"Error: {response_global.status_code} - {response_global.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_games_and_name_of_specific_gen_or_cat(games,all_games_infos, gen_or_cat, specific):
    column = 'genres' if 'genres' in gen_or_cat.columns else 'categories'
    # Filter gen_or_cat DataFrame to include only app_ids present in games
    filtered_gen_or_cat = gen_or_cat[gen_or_cat['app_id'].isin(games['app_id'])]
    # Filter the DataFrame to include only the specific genre or category
    specific_gen_or_cat = filtered_gen_or_cat[filtered_gen_or_cat[column] == specific]
    # Get the app_ids of the games that fall under the specific genre or category
    specific_games = specific_gen_or_cat['app_id']
    # Filter the games DataFrame to include only the games that fall under the specific genre or category
    specific_games_df = games[games['app_id'].isin(specific_games)]
    # Merging the two datasets on 'app_id' column
    merged_df = pd.merge(specific_games_df, all_games_infos[['app_id', 'name']], on='app_id')
    #sort by playtime_forever
    merged_df = merged_df.sort_values(by='playtime_forever', ascending=False)
    return merged_df

def get_n_best_gen_or_cat(games, gen_or_cat, n=6):
    column = 'genres' if 'genres' in gen_or_cat.columns else 'categories'
    # Filter gen_or_cat DataFrame to include only app_ids present in games
    filtered_gen_or_cat = gen_or_cat[gen_or_cat['app_id'].isin(games['app_id'])]
    # Count occurrences in filtered DataFrame
    gen_or_cat_counts = filtered_gen_or_cat[column].value_counts()
    # Get the first n categories or genres
    top_n = gen_or_cat_counts.head(n).to_dict()
    return top_n

def get_all_gen_or_cat(games, gen_or_cat):
    column = 'genres' if 'genres' in gen_or_cat.columns else 'categories'
    # Filter gen_or_cat DataFrame to include only app_ids present in games
    filtered_gen_or_cat = gen_or_cat[gen_or_cat['app_id'].isin(games['app_id'])]
    # Count occurrences in filtered DataFrame
    gen_or_cat_counts = filtered_gen_or_cat[column].value_counts()
    # Get the first n categories or genres
    all_gen_or_cat = gen_or_cat_counts.to_dict()
    return all_gen_or_cat

def get_n_best_gen_or_cat_by_hours(games, gen_or_cat, n=6):
    # Determine the grouping column dynamically
    grouping_column = 'genres' if 'genres' in gen_or_cat.columns else 'categories'
    # Merge games DataFrame with gen_or_cat DataFrame on 'app_id'
    merged_df = pd.merge(games, gen_or_cat, on='app_id', how='inner')
    # Calculate total playtime for each category or genre
    playtime_by_gen_or_cat = merged_df.groupby(grouping_column)['playtime_forever'].sum().reset_index() 
    # Sort by playtime in descending order
    playtime_by_gen_or_cat_sorted = playtime_by_gen_or_cat.sort_values(by='playtime_forever', ascending=False)
    # Get the top n categories or genres by playtime
    top_n = playtime_by_gen_or_cat_sorted.head(n)
    # Convert the DataFrame to a dictionary where genre/category is associated with the number of hours
    result = {row[grouping_column]: row['playtime_forever'] for index, row in top_n.iterrows()}
    return result

def get_all_gen_or_cat_by_hours(games, gen_or_cat):
    # Determine the grouping column dynamically
    grouping_column = 'genres' if 'genres' in gen_or_cat.columns else 'categories'
    # Merge games DataFrame with gen_or_cat DataFrame on 'app_id'
    merged_df = pd.merge(games, gen_or_cat, on='app_id', how='inner')
    # Calculate total playtime for each category or genre
    playtime_by_gen_or_cat = merged_df.groupby(grouping_column)['playtime_forever'].sum().reset_index() 
    # Sort by playtime in descending order
    playtime_by_gen_or_cat_sorted = playtime_by_gen_or_cat.sort_values(by='playtime_forever', ascending=False)
    # Convert the DataFrame to a dictionary where genre/category is associated with the number of hours
    result = {row[grouping_column]: row['playtime_forever'] for index, row in playtime_by_gen_or_cat_sorted.iterrows()}
    return result
