import pandas as pd
import requests

def load_data(file_path):
    return pd.read_csv(file_path)

def get_game_list_from_api(player_id):
    print("Getting games from API")
    api_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=5E613902A6191613402845D8EDD65A1C&steamid={player_id}&format=json"

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
    
def get_n_best_gen_or_cat(games, gen_or_cat, n=6):
    column = 'genres' if 'genres' in gen_or_cat.columns else 'categories'
    # Filter gen_or_cat DataFrame to include only app_ids present in games
    filtered_gen_or_cat = gen_or_cat[gen_or_cat['app_id'].isin(games['app_id'])]
    # Count occurrences in filtered DataFrame
    gen_or_cat_counts = filtered_gen_or_cat[column].value_counts()
    # Get the first n categories or genres
    top_n = gen_or_cat_counts.head(n).to_dict()
    return top_n

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