from utils.data_processing import load_data, get_game_list_from_api

# Load the Steam games dataset
cleaned_games = load_data('data/cleaned_games.csv')
categories = load_data('data/categories.csv')
genres = load_data('data/genres.csv')
supported_languages = load_data('data/supported_languages.csv')
full_audio_languages = load_data('data/full_audio_languages.csv')
current_user_games = get_game_list_from_api('76561198150561997')

def update_user_data(steamid):
    current_user_games = get_game_list_from_api(steamid)
    # Update other fields related to user data from steam api here
