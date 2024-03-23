import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from components.top_games_chart import generate_top_games_chart
from layouts.home_layout import generate_home_layout
from utils.data_processing import load_data

# Load the Steam games dataset
data = load_data('data/games_exploded.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Define callback to update page content based on URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/home':
        return generate_home_layout(data)
    # Add more pages as needed
    else:
        return '404 - Page not found'

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
