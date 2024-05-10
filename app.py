import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from components.top_games_chart import generate_top_games_chart
from layouts.home_layout import generate_home_layout
from layouts.profile_layout import generate_profile_layout
from utils.load_data import cleaned_games, categories, genres, supported_languages, full_audio_languages

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
        return generate_home_layout()
    if pathname == '/profile':
        return generate_profile_layout()
    # Add more pages as needed
    else:
        return '404 - Page not found'

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
