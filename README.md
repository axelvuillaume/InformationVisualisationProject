# Information Visualisation Project - Steam Dashboard

## How to install?
To install the project, follow these steps:

### pip install

1. `pip install dash_bootstrap_components`

1. Put the `games.csv` and `games.json` files in the `data` folder.
2. Run the `steam-game-date-transformation.ipynb` notebook.
3. This will generate the following files: `categories.csv`, `cleaned_games.csv`, `full_audio_languages.csv`, `genres.csv`, and `supported_languages.csv`.
4. In order to get the grouped by CSV-files run `./utils/initialise_data.py`. It is important that the `is_done` dictionary has all values on `False` for all groupings to be done.

To run the project, execute the `app.py` file.

## Authors
Laurens
Ward
Oruç
Axel