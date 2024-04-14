from utils.data_processing import load_data

# Load the Steam games dataset
cleaned_games = load_data('data/cleaned_games.csv')
categories = load_data('data/categories.csv')
genres = load_data('data/genres.csv')
supported_languages = load_data('data/supported_languages.csv')
full_audio_languages = load_data('data/full_audio_languages.csv')