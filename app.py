import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from components.top_games_chart import generate_top_games_chart
from layouts.home_layout import generate_home_layout
from utils.data_processing import load_data

# Load the Steam games dataset
cleaned_games = load_data('data/cleaned_games.csv')
categories = load_data('data/categories.csv')
genres = load_data('data/genres.csv')
supported_languages = load_data('data/supported_languages.csv')
full_audio_languages = load_data('data/full_audio_languages.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# External CSS stylesheets
global_style = ['assets/styles.css']

# Define the app layout
app.layout = html.Div(
    id='layout',
    children=[
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')]  
)

# Define callback to update page content based on URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/home':
        return generate_home_layout(cleaned_games)
    # Add more pages as needed
    else:
        return '404 - Page not found'

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
